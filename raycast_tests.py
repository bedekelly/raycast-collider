from unittest import TestCase

from raycast import Polygon, Line, distance_from, pairs, FloatRange


class TestDistanceFrom(TestCase):
    def test_distance_from(self):
        class BasicPoint:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        o = BasicPoint(3, 4)
        self.assertEqual(distance_from(0, 0)(o), 5)


class TestIntersection(TestCase):
    def test_no_intersection(self):
        line1 = Line(((0, 0), (0, 1)))
        line2 = Line(((1, 0), (1, 1)))
        self.assertIsNone(line1.intersection_with(line2))

    def test_intersection_at_origin(self):
        line1 = Line(((1, 1), (2, 2)))
        line2 = Line(((1, -1), (-1, 1)))
        intersection = line1.intersection_with(line2)
        self.assertEqual(intersection.y, 0)
        self.assertEqual(intersection.x, 0)


class TestPairs(TestCase):
    def test_pairs(self):
        p = pairs((1, 2, 3))
        self.assertEqual(list(p), [(1, 2), (2, 3), (3, 1)])


class TestLine(TestCase):
    def test_from_angle(self):
        l = Line.from_angle(0, 0, 0, 2)
        self.assertEqual(l.x2, 0)
        self.assertEqual(l.y2, 2)

    def test_domain(self):
        l = Line(((0, 0), (1, 2)))
        self.assertTrue(0.5 in l.domain)
        self.assertFalse(-5 in l.domain)
        self.assertFalse(1.5 in l.domain)

    def test_range(self):
        l = Line(((0, 0), (1, 2)))
        self.assertTrue(1.5 in l.range)
        self.assertTrue(2 in l.range)
        self.assertFalse(-0.5 in l.range)
        self.assertFalse(3 in l.range)

    def test_eq(self):
        l1 = Line(((0, 0), (1, 1)))
        l2 = Line(((0, 0,), (1, 1)))
        l3 = Line(((0, 0), (2, 2)))
        l4 = Line(((0, 0), (1, 0)))
        self.assertEqual(l1, l2)
        self.assertNotEqual(l1, l3)
        self.assertNotEqual(l1, l4)
        self.assertNotEqual(l2, l4)


class TestFloatRange(TestCase):
    def setUp(self):
        self.my_range = FloatRange(0.0, 1.0)

    def test_in_range(self):
        self.assertTrue(0.4 in self.my_range)
        self.assertTrue(0 in self.my_range)
        self.assertTrue(1 in self.my_range)

    def test_out_of_range(self):
        self.assertFalse(-1.0 in self.my_range)
        self.assertFalse(1.9 in self.my_range)
        self.assertFalse(-0.3 in self.my_range)


class TestPolygon(TestCase):
    def setUp(self):
        self.p = Polygon(name="PolyName", points=((0, 0), (0, 1), (1, 1)))

    def test_str(self):
        self.assertEqual(str(self.p), "PolyName")

    def test_lines(self):
        self.assertEqual(
            list(self.p.lines),
            [
                Line(((0, 0), (0, 1)), self.p),
                Line(((0, 1), (1, 1)), self.p),
                Line(((1, 1), (0, 0)), self.p)
            ]
        )
