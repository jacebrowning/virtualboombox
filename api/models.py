from math import radians, degrees, cos, sin, asin, atan2, sqrt


AVERAGE_EARTH_RADIUS = 3959


def calculate_haversine(point1, point2):
    """Calculate the great-circle distance between two locations."""

    # Unpack latitude/longitude
    lat1, long1 = point1
    lat2, long2 = point2

    # Convert to radians
    lat1, long1, lat2, long2 = map(radians, (lat1, long1, lat2, long2))

    # Calculate haversine distance
    Δlat = lat2 - lat1
    Δlong = long2 - long1
    d = sin(Δlat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(Δlong * 0.5) ** 2
    distance = 2 * AVERAGE_EARTH_RADIUS * asin(sqrt(d))

    return distance


def calculate_bearing(point1, point2):
    """Calculate the bearing between two locations."""

    # Unpack latitude/longitude
    lat1, long1 = point1
    lat2, long2 = point2

    # Convert all latitudes/longitudes from decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, (lat1, long1, lat2, long2))

    # Calculate bearing
    Δlong = (long2 - long1)

    x = sin(Δlong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(Δlong)

    # Normalize and convert to degrees
    initial_bearing_radians = atan2(x, y)
    initial_bearing_degrees = degrees(initial_bearing_radians)
    compass_bearing_degrees = (initial_bearing_degrees + 360) % 360

    return compass_bearing_degrees


class QueuedSong:

    def __init__(self, song, this_location, that_location=None):
        self.song = song
        self.this_location = this_location
        self._that_location = that_location

    @property
    def id(self):
        return self.song.id

    @property
    def that_location(self):
        return self._that_location or self.song.location

    @property
    def distance(self):
        return calculate_haversine(self.this_location, self.that_location)

    @property
    def angle(self):
        return calculate_bearing(self.this_location, self.that_location)

    @property
    def data(self):
        return dict(
            artist=self.song.artist,
            title=self.song.title,
            miles=f"{self.distance:.1f}",
            degrees=self.angle,
            youtube_url=self.song.youtube_url,
        )
