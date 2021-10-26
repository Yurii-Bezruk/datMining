import math
import random
from typing import List
from matplotlib import pyplot as plt


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}; {self.y})'

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y


class Cluster:

    def __init__(self, center: Point):
        self.center = center
        self.points: List[Point] = []

    def __str__(self):
        return f'Center: {self.center}\nPoints: [{", ".join([_point.__str__() for _point in self.points])}]'

    def add(self, _point: Point):
        self.points.append(_point)
        self.refresh_center()

    def remove(self, _point: Point):
        self.points.remove(_point)
        self.refresh_center()

    def clear(self):
        self.points.clear()

    def refresh_center(self):
        if len(self.points) > 0:
            x = sum([_point.x for _point in self.points]) / len(self.points)
            y = sum([_point.y for _point in self.points]) / len(self.points)
            self.center = Point(x, y)


def load_points(_filename: str) -> List[Point]:
    file = open(_filename, 'r')
    _points = []
    counter = 0
    for line in file:
        if counter == 10000:
            break
        line = line.strip().split(" ")
        _points.append(Point(int(line[0]), int(line[-1])))
        counter += 1
    return _points


def cluster_iterations(_cluster_count: int, _points: List[Point]):
    _clusters = []
    deviations = []
    for i in range(1, _cluster_count + 1):
        _clusters = random_clusters(i, points)
        match_to_clusters(points, _clusters)
        re_clustering(_clusters)
        deviations.append(total_square_deviation(_clusters))
    view_clusters(_clusters)
    view_deviations(deviations)


def random_clusters(_cluster_count: int, _points: List[Point]) -> List[Cluster]:
    x = [pt.x for pt in _points]
    y = [pt.y for pt in _points]
    max_x = max(x)
    min_x = min(x)
    max_y = max(y)
    min_y = min(y)
    _clusters = []
    for i in range(_cluster_count):
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        _clusters.append(Cluster(Point(x, y)))
    return _clusters


def euclid_distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def match_to_clusters(_points: List[Point], _clusters: List[Cluster]):
    for _point in points:
        min_distance_cluster = min(_clusters, key=lambda _cluster: euclid_distance(_point, _cluster.center))
        min_distance_cluster.add(_point)


def re_clustering(_clusters: List[Cluster]):
    moved: bool = True
    while moved:
        moved = False
        for _cluster in _clusters:
            for _point in _cluster.points:
                min_distance_cluster = min(_clusters, key=lambda _cluster: euclid_distance(_point, _cluster.center))
                if min_distance_cluster != _cluster:
                    _cluster.remove(_point)
                    min_distance_cluster.add(_point)
                    moved = True


def total_square_deviation(_clusters: List[Cluster]) -> int:
    deviation = 0
    for _cluster in _clusters:
        for _point in _cluster.points:
            deviation += (_point.x - _cluster.center.x) ** 2
            deviation += (_point.y - _cluster.center.y) ** 2
    return deviation


def view_points(_points: List[Point]):
    plt.scatter([pt.x for pt in _points], [pt.y for pt in _points])
    plt.title('Points from dataset')
    plt.show()


def view_clusters(_clusters: List[Cluster]):
    for _cluster in _clusters:
        plt.scatter([pt.x for pt in _cluster.points], [pt.y for pt in _cluster.points])
        plt.scatter([_cluster.center.x], [_cluster.center.y], c='black')
    plt.title('Clustered points')
    plt.show()


def view_deviations(_deviations: list):
    plt.plot([i for i in range(1, len(_deviations) + 1)], _deviations)
    plt.title('Total square deviation')
    plt.xlabel('Clusters count')
    plt.ylabel('Deviation')
    plt.show()


print('Enter name of file with dataset: ', end='')
filename = input()
print('Enter number of clusters: ', end='')
cluster_count = int(input())
points = load_points(filename)
view_points(points)
cluster_iterations(cluster_count, points)

