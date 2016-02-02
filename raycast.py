"""
raycast: Implement a basic raycasting collision-detection algorithm.
Given an arbitrary set of polygons, and a starting point and angle for the
detection ray, return the first polygon the ray collides with.
"""
from collections import deque, namedtuple
from math import cos, sin, hypot


def pairs(items):
    """Generate a sequence of pairs from a sequence:
    pairs([a, b, c]) -> [(a,b), (b,c), (c,a)]
    :param items: A sequence of items to pair."""
    items_r = deque(items)
    items_r.rotate(-1)
    return zip(items, items_r)


Intersection = namedtuple("Intersection", "x y shapes")


class FloatRange:
    """Define a range by declaring an upper and lower bound:
    float(...) in FloatRange(...) -> bool"""

    def __init__(self, lower=0, upper=0):
        self.lower = lower
        self.upper = upper

    def __eq__(self, other):
        return self.lower == other.lower and self.upper == other.upper

    def __contains__(self, item):
        return self.lower <= item <= self.upper


class Line:
    """Represent a Line as a pair of (X, Y) points, and provide methods for
    assessing the domain and range of this line, and for generating information
    about intersections with other given lines."""

    def __init__(self, pair, shape=None):
        self.shape = shape
        (self.x1, self.y1), (self.x2, self.y2) = pair
        try:
            self.gradient = (self.y2 - self.y1) / (self.x2 - self.x1)
            self.y_intercept = self.y1 - self.gradient * self.x1
        except ZeroDivisionError:
            # The line is parallel to the Y-axis.
            self.gradient = float("inf")
            self.y_intercept = float("inf")

    def __eq__(self, other):
        return all((
            self.gradient == other.gradient,
            self.y_intercept == other.y_intercept,
            self.domain == other.domain,
            self.range == other.range
        ))

    @staticmethod
    def from_angle(x1, y1, angle, length):
        """Create a line from a point (x, y) and some angle in radians.
        :param length: The length of our new line.
        :param angle: The angle our line subtends clockwise from due north.
        :param y1: The Y coordinate of the given point.
        :param x1: The X coordinate of the given point.
        """
        x2 = x1 + length * sin(angle)
        y2 = y1 + length * cos(angle)
        return Line(((x1, y1), (x2, y2)))

    @property
    def domain(self):
        """Returns the domain of X values for this line."""
        lower, upper = sorted((self.x1, self.x2))
        return FloatRange(lower=lower, upper=upper)

    @property
    def range(self):
        """Returns the range of Y values for this line."""
        lower, upper = sorted((self.y1, self.y2))
        return FloatRange(lower=lower, upper=upper)

    def intersection_with(self, other):
        """Return the Intersection between this line and `other`. Don't take
        the domain or range of either line into account; assume the lines
        extend to infinity.
        :param other: The line with which this line may intersect.
        """

        if self.gradient == other.gradient:
            # Lines of the same gradient never intersect.
            return None

        # Calculate the X and Y values of this intersection using linear algebra.
        x = (other.y_intercept - self.y_intercept) / (self.gradient - other.gradient)
        y = self.gradient * x + self.y_intercept

        # If this or the other line belong to a shape, add it to a new set of shapes
        # involved in this intersection.
        shapes = filter((lambda o: o is not None), (self.shape, other.shape))
        return Intersection(x, y, shapes)


class Polygon:
    """A Polygon is an ordered collection of (x, y) points.
    From these points, it can also generate a sequence of lines,
    including domains and ranges."""

    def __init__(self, name=None, points=()):
        self.points = points
        self.name = name

    def __str__(self):
        return self.name

    @property
    def lines(self):
        """Yields a Line for each pair of points in the polygon."""
        for pair in pairs(self.points):
            yield Line(pair, shape=self)


def distance_from(x, y):
    def key(o):
        """Returns the distance from (x, y) to object o.
        :param o: The object to which we calculate the distance.
        """
        return hypot((x - o.x), (y - o.y))

    return key
