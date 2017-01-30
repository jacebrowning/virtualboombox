from math import radians, cos, sin, asin, sqrt


AVERAGE_EARTH_RADIUS = 3959


def haversine(point1, point2):
    """Calculate the great-circle distance between two points."""

    # Unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # Convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # Calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    distance = 2 * AVERAGE_EARTH_RADIUS * asin(sqrt(d))

    return distance
