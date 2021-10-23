import math
from typing import List


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}; {self.y})'

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

class Cluster:

    def __init__(self, center: Point):
        self.center = center
        self.__points = []

    def __str__(self):
        return f'Center: {self.center}\nPoints: [{", ".join([point.__str__() for point in self.__points])}]'

    def __eq__(self, c):
        return self.__points == c.__points

    def add(self, point: Point):
        self.__points.append(point)

    def refresh_center(self):
        x = sum([point.x for point in self.__points]) / len(self.__points)
        y = sum([point.y for point in self.__points]) / len(self.__points)
        self.center = Point(x, y)


def load_points(filename: str) -> List[Point]:
    file = open(filename, 'r')
    _points = []
    for line in file:
        line = line.strip().split(" ")
        _points.append(Point(int(line[0]), int(line[-1])))
    return _points


def random_clusters(_cluster_count: int, _points: List[Point]) -> List[Cluster]:
    _max = len(_points)
    step = int(_max / _cluster_count)
    _clusters = []
    for i in range(0, _max, step):
        _clusters.append(Cluster(_points[i]))
    return _clusters


def euclid_distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def match_to_clusters(points: List[Point], clusters: List[Cluster]) -> List[Cluster]:
    for point in points:
        min_distance = euclid_distance(point, clusters[0].center)
        for cluster in clusters:
            if euclid_distance(point, cluster.center) < min_distance:
                cluster.add(point)
    return clusters


def clustering(points: List[Point], clusters: List[Cluster]):
    new_clusters = match_to_clusters(points, clusters.copy())
    # while new_clusters


cluster_count = 3
points = load_points('test.txt')
clusters = random_clusters(cluster_count, points)
match_to_clusters(points, clusters)

for point in points:
    print(f'{point.x} {point.y}')
print('hi')
for cluster in clusters:
    print(cluster)

