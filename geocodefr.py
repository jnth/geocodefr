#!/usr/bin/env python3.6
# coding: utf-8

"""Geocode addresse using the BAN (Base Adresse Nationale)."""


import requests
import pyproj
from shapely.geometry import asShape


__version__ = '0.1'


# Type of level
HOUSENUMBER = 1  # au numéro
STREET = 2  # à la rue
MUNICIPALITY = 3  # lieu-dit


_type = {
    HOUSENUMBER: 'housenumber',
    STREET: 'street',
    MUNICIPALITY: 'municipality'
}


class Feature:
    """Feature."""

    def __init__(self, data):
        """Feature."""
        self.data = data
        self.pll = pyproj.Proj(init='epsg:4326')  # wgs84

    @property
    def properties(self):
        """Properties of the feature."""
        return self.data["properties"]

    @property
    def geometry(self):
        """Geometry of the feature."""
        return asShape(self.data["geometry"])

    @property
    def lon(self):
        """Longitude of the feature."""
        return self.geometry.x

    @property
    def lat(self):
        """Latitude of the feature."""
        return self.geometry.y

    @property
    def citycode(self):
        """City code."""
        return self.properties['citycode']

    def __str__(self):
        return self.properties['label']

    def __repr__(self):
        return "<Feature '{}>".format(self)

    def transform(self, epsg):
        """Reprojection into another system.
        
        :param epsg: EPSG code (int).
        :return: (x, y).
        """
        p = pyproj.Proj(init='epsg:{}'.format(epsg))
        return pyproj.transform(self.pll, p, self.lon, self.lat)


class GeocodeFrError(Exception):
    pass


class GeocodeFr:
    """Geocode addresse using the BAN (Base Adresse Nationale)."""

    def __init__(self):
        """Geocode addresse using the BAN (Base Adresse Nationale)."""
        self.url = 'http://api-adresse.data.gouv.fr'

    def _get(self, path, params):
        """GET request."""
        r = requests.get(self.url + path, params=params)
        r.raise_for_status()
        return r.json()

    def search(self, query, limit=None, level=None):
        """Geocode an address.

        :param query: query as string.
        :param limit:
        :param level: type of level.
        :return:
        """
        if level and level not in _type:
            raise GeocodeFrError("Cannot reconize level.")

        params = {'q': query}
        if limit:
            params['limit'] = limit
        if level:
            params['type'] = _type[level]

        res = self._get('/search', params)
        return [Feature(e) for e in res['features']]

    def reverse(self, lon, lat, level=None):
        """Reverse geocoding.
        
        :param lon: longitude (float).
        :param lat: latitude (float).
        :param level: type of level.
        :return:
        """
        if level and level not in _type:
            raise GeocodeFrError("Cannot reconize level.")

        params = {'lon': lon, 'lat': lat}
        if level:
            params['type'] = _type[level]

        res = self._get('/reverse', params)
        return [Feature(e) for e in res['features']]


