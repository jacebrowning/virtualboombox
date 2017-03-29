from math import radians, degrees, cos, sin, asin, atan2, sqrt

from django.utils import timezone


AVERAGE_EARTH_RADIUS = 3959

PLACEHOLDER_YOUTUBE_URL = "https://www.youtube.com/v/dQw4w9WgXcQ"


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

    WEIGHT_DISTANCE = 0.5
    WEIGHT_TIME = 0.5

    def __init__(self, song, this_location, that_location=None):
        self.song = song
        self.this_location = this_location
        self._that_location = that_location
        self._distance = None
        self._elapsed_time = None

    @property
    def ref(self):
        return self.song.ref

    @property
    def that_location(self):
        return self._that_location or self.song.location

    @property
    def elapsed_time(self):
        if self._elapsed_time is None:
            delta = timezone.now() - self.song.date
            return delta.days * 24 * 60 + delta.seconds / 60
        else:
            return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, value):
        self._elapsed_time = value

    @property
    def distance(self):
        if self._distance is None:
            return calculate_haversine(self.this_location, self.that_location)
        else:
            return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value

    @property
    def score(self):
        return round(sum([
            self._scale_distance(self.distance, self.WEIGHT_DISTANCE),
            self._scale_time(self.elapsed_time, self.WEIGHT_TIME),
        ]), 3)

    @staticmethod
    def _scale_distance(value, weight):
        """Scale distance between 0 and 1 with optional weighting.

        0 to 1/2 mile (walking distance)        => 1
        12,450 miles (1/2 earth circumference)  => 0

        """
        lower = 0.5
        upper = 12450 - lower

        value = max(value - lower, 0)
        value = min(value, upper)

        return (1 - value / upper) * weight

    @staticmethod
    def _scale_time(value, weight):
        """Scale elapsed time between 0 and 1 with optional weighting.

        0 to 5 minutes (song still playing)     => 1
        1,440 minutes (1 day)                   => 0

        """
        lower = 5
        upper = 1440 - lower

        value = max(value - lower, 0)
        value = min(value, upper)

        return (1 - value / upper) * weight

    @property
    def angle(self):
        return calculate_bearing(self.this_location, self.that_location)

    @property
    def data(self):
        if self.distance < 20:
            miles = f"{self.distance:.1f}"
        else:
            miles = str(round(self.distance))

        return dict(
            artist=self.song.artist,
            title=self.song.title,
            miles=miles,
            degrees=self.angle,
            lastfm_url=self.song.lastfm_url,
            youtube_url=self.song.youtube_url or PLACEHOLDER_YOUTUBE_URL,
            ref=str(self.ref),
        )
