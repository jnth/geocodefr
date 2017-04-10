#!/usr/bin/env python3.6
# coding: utf-8

"""Tests."""


import unittest
import requests
import responses
import geocodefr


class TestGeocodeFr(unittest.TestCase):
    @responses.activate
    def test_responses(self):
        responses.add(responses.GET, 'http://api.com/spam',
                      body='{"status": "spam"}',
                      content_type='application/json')

        r = requests.get('http://api.com/spam')
        self.assertEqual(r.json(), {"status": "spam"})

    @responses.activate
    def test_search(self):
        with open('testdata/test.json') as f:
            responses.add(responses.GET,
                          'http://api-adresse.data.gouv.fr/search',
                          body=f.read(), content_type='application/json')
        geo = geocodefr.GeocodeFr()
        features = geo.search("Marseille")
        self.assertEqual(len(features), 5)

        f = features[0]
        self.assertIsInstance(f, geocodefr.Feature)
        self.assertEqual(f.citycode, '13206')
        self.assertEqual(f.geometry.type, 'Point')
        self.assertAlmostEqual(f.lon, 5.379505, delta=0.0001)
        self.assertAlmostEqual(f.lat, 43.286783, delta=0.0001)
        self.assertEqual(str(f), "146 Rue Paradis 13006 Marseille")
        self.assertTrue("146 Rue Paradis 13006 Marseille" in repr(f))
        x, y = f.transform(2154)
        self.assertAlmostEqual(x, 893210.4, delta=1)
        self.assertAlmostEqual(y, 6245979.2, delta=1)

    def test_search_error(self):
        geo = geocodefr.GeocodeFr()
        with self.assertRaises(geocodefr.GeocodeFrError):
            geo.search("Marseille", level=-1)

    @responses.activate
    def test_search_limit(self):
        with open('testdata/test_limit.json') as f:
            responses.add(responses.GET,
                          'http://api-adresse.data.gouv.fr/search',
                          body=f.read(), content_type='application/json')
        geo = geocodefr.GeocodeFr()
        features = geo.search("Marseille", limit=1)
        self.assertEqual(len(features), 1)

    @responses.activate
    def test_search_level(self):
        with open('testdata/test_level.json') as f:
            responses.add(responses.GET,
                          'http://api-adresse.data.gouv.fr/search',
                          body=f.read(), content_type='application/json')
        geo = geocodefr.GeocodeFr()
        features = geo.search("Marseille", level=geocodefr.MUNICIPALITY)
        f = features[0]
        self.assertEqual(f.citycode, '13055')

    @responses.activate
    def test_reverse(self):
        with open('testdata/test_reverse.json') as f:
            responses.add(responses.GET,
                          'http://api-adresse.data.gouv.fr/reverse',
                          body=f.read(), content_type='application/json')
        geo = geocodefr.GeocodeFr()
        features = geo.reverse(lon=2.37, lat=48.357)
        f = features[0]
        self.assertEqual(f.citycode, '91507')
        self.assertEqual(f.properties['label'],
                         "6 Rue de l'Église 91720 Prunay-sur-Essonne")

    @responses.activate
    def test_reverse_level(self):
        with open('testdata/test_reverse_level.json') as f:
            responses.add(responses.GET,
                          'http://api-adresse.data.gouv.fr/reverse',
                          body=f.read(), content_type='application/json')
        geo = geocodefr.GeocodeFr()
        features = geo.reverse(lon=2.37, lat=48.357,
                               level=geocodefr.STREET)
        f = features[0]
        self.assertEqual(f.citycode, '91507')
        self.assertEqual(f.properties['label'],
                         "Rue des Ouches 91720 Prunay-sur-Essonne")

    def test_reverse_error(self):
        geo = geocodefr.GeocodeFr()
        with self.assertRaises(geocodefr.GeocodeFrError):
            geo.reverse(2.37, 48.357, level=-1)


if __name__ == '__main__':
    unittest.main()
