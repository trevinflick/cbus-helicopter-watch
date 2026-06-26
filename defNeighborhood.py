import json

_communities = None

def _load_communities():
    global _communities
    if _communities is None:
        from shapely.geometry import shape
        with open('./dependencies/columbus_communities.geojson', 'r', encoding='utf-8') as f:
            geojson = json.load(f)
        _communities = [
            (feature['properties']['AREA_NAME'], shape(feature['geometry']))
            for feature in geojson['features']
        ]
    return _communities

def get_neighborhood(latitude, longitude):
    """Returns the Columbus community/neighborhood name containing this point, or None
    if the point falls outside all mapped boundaries (e.g. just outside city limits)."""
    from shapely.geometry import Point
    point = Point(longitude, latitude)
    for name, polygon in _load_communities():
        if polygon.contains(point):
            return name
    return None
