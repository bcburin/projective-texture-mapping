from enum import Enum, auto
from itertools import permutations

import numpy as np
from numpy import array


class Orientation(Enum):
    COLLINEAR_POINTS = auto()
    CLOCKWISE = auto()
    COUNTER_CLOCKWISE = auto()


def get_orientation(p: array, q: array, r: array) -> Orientation:
    val = np.cross(q-p, r-q)
    if val == 0:
        return Orientation.COLLINEAR_POINTS
    return Orientation.CLOCKWISE if val > 0 else Orientation.COUNTER_CLOCKWISE


class Polygon:
    _points: list[array]

    def __init__(self, points: list[array]):
        self._points = self.get_simple_polygon(points)

    @staticmethod
    def is_simple_polygon(points: list[array]) -> bool:
        if len(points) < 3:
            return False
        orientation_flag = None
        for i in range(len(points)):
            p = points[i]
            q = points[(i + 1) % len(points)]
            r = points[(i + 2) % len(points)]
            orientation = get_orientation(p, q, r)
            if orientation == Orientation.COLLINEAR_POINTS:
                return False
            if orientation_flag is None:
                orientation_flag = orientation
            elif orientation_flag != orientation:
                return False
        return True

    @staticmethod
    def invert_polygon_orientation(points: list[array]) -> list[array]:
        n = len(points)
        inverted = [points[0]]
        inverted.extend([points[n - 1 - i] for i in range(n - 1)])
        return inverted

    @classmethod
    def get_simple_polygon(cls, points: list[array]) -> list[array]:
        for point_ordering in permutations(points):
            point_ordering_list = list(point_ordering)
            if cls.is_simple_polygon(points=point_ordering_list):
                return point_ordering_list
        raise ValueError("Cannot form polygon")

    def as_list(self, orientation: Orientation | None = None):
        p_orientation = get_orientation(self._points[0], self._points[1], self._points[2])
        if p_orientation is None or p_orientation == orientation:
            return self._points
        else:
            return self.invert_polygon_orientation(self._points)
