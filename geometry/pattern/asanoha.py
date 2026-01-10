from typing import List, Union

from geometry.pattern.pattern import Pattern
from geometry.primitives import Line, Arc, QuadraticBezier


class AsanohaPattern(Pattern):
    def get_material_cost(self):
        return 2.0

    def _get_geometry(self, a, b, c) -> List[Union[Line, Arc, QuadraticBezier]]:
        ax, ay = a
        bx, by = b
        cx, cy = c

        # Calculate centroid
        centroid_x = (ax + bx + cx) / 3
        centroid_y = (ay + by + cy) / 3

        return [
            Line((centroid_x, centroid_y), (ax, ay)),
            Line((centroid_x, centroid_y), (bx, by)),
            Line((centroid_x, centroid_y), (cx, cy))
        ]

