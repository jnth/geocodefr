#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from geocodefr import __version__

setup(
    name='geocodefr',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/jnth/geocodefr',
    license='GNU GPLv3',
    author='Jonathan Virga',
    author_email='jonathan.virga@gmail.com',
    description=('French address geocoding with the BAN '
                 '(Base Adresse Nationale).'),
    long_description=open('README.md').read(),
    requires=['requests', 'pyproj', 'shapely']
)
