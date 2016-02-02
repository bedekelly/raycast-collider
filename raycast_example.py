from math import atan
from raycast import Polygon, Line, distance_from

X = 0
Y = 0
ANGLE = atan(1.999)
MAX_LINE = 100

square1 = Polygon(name="A", points=((1, 1), (1, 2), (2, 2), (2, 1)))
square2 = Polygon(name="B", points=((3, 3), (3, 4), (4, 4), (4, 3)))
graph = {square1, square2}

ray = Line.from_angle(0, 0, ANGLE, MAX_LINE)
intersections = set()
for polygon in graph:
    for line in polygon.lines:
        i = line.intersection_with(ray)
        if i is None:
            continue
        if i.x not in line.domain or i.y not in line.range:
            continue
        intersections.add(i)

if intersections:
    min_intersection = min(intersections, key=distance_from(X, Y))
    for s in min_intersection.shapes:
        print("Ray collided with", s)

