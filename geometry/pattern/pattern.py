import math
from abc import ABC, abstractmethod
from typing import List, Union

from geometry.primitives import Line, Arc, QuadraticBezier


class Pattern(ABC):
    def __init__(self, stroke="red", stroke_width=1, rotation=0):
        self.rotation = rotation
        self.stroke = stroke
        self.stroke_width = stroke_width

    def _shift_points(self, points):
        # (a, b, c)
        # Rotate points by pattern_rotation * 120 degrees by reordering
        # rotation 0 = (a, b, c)
        # rotation 1 = (b, c, a)
        # rotation 2 = (c, a, b)
        rotation = self.rotation % 3
        return points[rotation:] + points[:rotation]

    @staticmethod
    def control_point(midpoint, centroid, magnitude=1):
        dx = centroid[0] - midpoint[0]
        dy = centroid[1] - midpoint[1]
        return (
            midpoint[0] + dx * magnitude,
            midpoint[1] + dy * magnitude
        )

    def get_geometry(self, a, b, c):
        points = self._shift_points((a, b, c))
        return self._get_geometry(*points)

    @abstractmethod
    def _get_geometry(self, a, b, c) -> List[Union[Line, Arc, QuadraticBezier]]:
        """Return a list of 2D geometric primitives (lines, arcs, etc.)"""

    @abstractmethod
    def get_material_cost(self) -> float:
        pass


