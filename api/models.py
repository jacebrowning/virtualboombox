from math import radians, degrees, cos, sin, asin, atan2, sqrt


AVERAGE_EARTH_RADIUS = 3959


def calculate_haversine(point1, point2):
    """Calculate the great-circle distance between two locations."""

    # Unpack latitude/longitude
    lat1, long1 = point1
    lat2, long2 = point2

    # Convert all latitudes/longitudes from decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, (lat1, long1, lat2, long2))

    # Calculate haversine
    lat = lat2 - lat1
    long = long2 - long1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(long * 0.5) ** 2
    distance = 2 * AVERAGE_EARTH_RADIUS * asin(sqrt(d))

    return distance


def calculate_bearing(point1, point2):
    """Calculate the bearing between two locations."""

    # Unpack latitude/longitude
    lat1, long1 = point1
    lat2, long2 = point2

    delta_long = (long2 - long1);

    y = sin(delta_long) * cos(lat2)
    x = cos(lat2) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_long)

    radians = atan2(y, x)

    return degrees(radians)


class QueuedSong:

    def __init__(self, song, base_location):
        self.artist = song.artist
        self.title = song.title
        self.location = float(song.latitude), float(song.longitude)
        self.base_location = base_location

    @property
    def distance(self):
        return calculate_haversine(self.base_location, self.location)

    @property
    def angle(self):
        return calculate_bearing(self.base_location, self.location)

    @property
    def data(self):
        return dict(
            artist=self.artist,
            title=self.title,
            miles=f"{self.distance:.1f}",
            degrees=self.angle,
        )
