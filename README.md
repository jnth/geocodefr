# GeocodeFr

## Utilisation 

Import et utilisation de la librairie :

    >>> import geocodefr
    >>> geo = geocodefr.GeocodeFr()

Recherche d'une adresse

    >>> geo.search("146 rue Paradis, Marseille")
    
Résultats sous la forme d'une liste de `Feature` :

    [<Feature '146 Rue Paradis 13006 Marseille>,
     <Feature 'Rue Paradis 13008 Marseille>,
     <Feature 'Rue Paradis 13001 Marseille>,
     <Feature 'Rue Villas Paradis 13006 Marseille>,
     <Feature 'Rue Villas Paradis 13008 Marseille>]

Utilisation d'un filtre sur le niveau géographique :
    
    >>> geo.search("Nice", level=geocodefr.MUNICIPALITY)
    
Afficher uniquement le 1er résultat :

    >>> geo.search("Nice", level=geocodefr.MUNICIPALITY, limit=1)
    
Géocodage inverse :

    >>> geo.reverse(0, 45)
    
Résultats sous la forme d'une liste de `Feature` :

    [<Feature '10 Chemin des Rossignols 33660 Saint-Seurin-sur-l'Isle>]
    
    
## Objet `Feature`

Résultat sous la forme d'un point (géométrie) et de données attributaires :

    >>> f = geo.reverse(0, 45)[0]
    
    >>> f.lon, f.lat
    (0.002064, 44.997674)
    
    >>> f.citycode
    '33478'
    
    >>> f.geometry.wkt
    'POINT (0.002064 44.997674)'
    
Reprojection dans un autre système de coordonnées :

    >>> f.transform(2154)
    (463811.4617467372, 6437644.824337756)
    
    
## Exemple d'utilisation

Recherche du code INSEE d'une commune :

    >>> import geocodefr
    >>> geo = geocodefr.GeocodeFr()
    >>> f = geo.search('Lyon', level=geocodefr.MUNICIPALITY)[0]  # 1st result
    >>> f.citycode
    '69123'
