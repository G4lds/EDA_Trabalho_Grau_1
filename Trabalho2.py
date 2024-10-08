from abc import ABC, abstractmethod
from typing import List
from typing import Optional

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class Node:
    def __init__(self, x: float, y: float, value: object) -> None:
        self.x = x
        self.y = y
        self.value = value
        self.NW: Optional[Node] = None
        self.NE: Optional[Node] = None
        self.SW: Optional[Node] = None
        self.SE: Optional[Node] = None
    def __str__(self) -> str:
        return "({}, {}) {}".format(self.x, self.y, self.value)


class Interval:
    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max
    def contains(self, x: float) -> bool:
        return self.min <= x <= self.max


class Interval2D:
    def __init__(self, interval_x: Interval, interval_y: Interval) -> None:
        self.interval_x = interval_x
        self.interval_y = interval_y
    def contains(self, x: float, y: float) -> bool:
        return self.interval_x.contains(x) and self.interval_y.contains(y)


class QuadTreeADT(ABC):
    @abstractmethod
    def clear(self) -> None: ...
    @abstractmethod
    def is_empty(self) -> bool: ...
    @abstractmethod
    def insert(self, x: object, y: object, value: object) -> None: ...
    @abstractmethod
    def query_2D(self, rect: Interval2D) -> None: ...
    @abstractmethod
    def search(self, point: Point) -> object: ...
    @abstractmethod
    def all_points(self) -> List[Point]: ...


class QuadTree:
    def __init__(self) -> None:
        self._root: Optional[Node] = None

    def clear(self) -> None:
        self._root = None

    def is_empty(self) -> bool:
        return self._root is None

    def insert(self, x: float, y: float, value: object) -> None:
        def insert(current: Optional[Node], x: float, y: float, value: object):
            if current is None:
                return Node(x, y, value)
            elif x < current.x and y >= current.y:
                current.NW = insert(current.NW, x, y, value)
            elif x < current.x and y < current.y:
                current.SW = insert(current.SW, x, y, value)
            elif x >= current.x and y >= current.y:
                current.NE = insert(current.NE, x, y, value)
            elif x >= current.x and y < current.y:
                current.SE = insert(current.SE, x, y, value)
            return current
        self._root = insert(self._root, x, y, value)

    def query_2D(self, rect: Interval2D) -> None:
        def query_2D(current, rect: Interval2D) -> None:
            if current is None:
                return
            x_min = rect.interval_x.min
            x_max = rect.interval_x.max
            y_min = rect.interval_y.min
            y_max = rect.interval_y.max
            if rect.contains(current.x, current.y):
                print(current)
            if x_min < current.x and y_max >= current.y:
                query_2D(current.NW, rect)
            if x_min < current.x and y_min < current.y:
                query_2D(current.SW, rect)
            if x_max >= current.x and y_max >= current.y:
                query_2D(current.NE, rect)
            if x_max >= current.x and y_min < current.y:
                query_2D(current.SE, rect)
        query_2D(self._root, rect)

    def search(self, point: Point) -> object:
        def search(current, point: Point) -> object:
            if current is None:
                return None
            if current.x == point.x and current.y == point.y:
                return current.value
            if point.x < current.x and point.y >= current.y:
                return search(current.NW, point)
            elif point.x < current.x and point.y < current.y:
                return search(current.SW, point)
            elif point.x >= current.x and point.y >= current.y:
                return search(current.NE, point)
            else:
                return search(current.SE, point)

        return search(self._root, point)

    def all_points(self) -> List[Point]:
        points = []
        def coleta_pontos(current) -> None:
            if current is None:
                return None
            points.append(Point(current.x, current.y))
            coleta_pontos(current.NW)
            coleta_pontos(current.SW)
            coleta_pontos(current.NE)
            coleta_pontos(current.SE)
        coleta_pontos(self._root)
        return points
