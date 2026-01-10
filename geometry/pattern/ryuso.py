from typing import List, Union

from geometry.pattern.pattern import Pattern
from geometry.primitives import Line, Arc, QuadraticBezier


class RyusoPattern(Pattern):
    def get_material_cost(self) -> float:
        return 3.2

    def _get_geometry(self, a, b, c) -> List[Union[Line, Arc, QuadraticBezier]]:
        ax, ay = a
        bx, by = b
        cx, cy = c

        # Midpoints of each side
        mid_ab = ((ax + bx) / 2, (ay + by) / 2)
        mid_bc = ((bx + cx) / 2, (by + cy) / 2)
        mid_ca = ((cx + ax) / 2, (cy + ay) / 2)

        return [
            # 1) Midpoints connected to opposite vertex
            Line(mid_ab, (cx, cy)),
            Line(mid_bc, (ax, ay)),
            Line(mid_ca, (bx, by)),

            # 2) Lines connecting midpoints to each other (forming inner triangle)
            Line(mid_ab, mid_bc),
            Line(mid_bc, mid_ca),
            Line(mid_ca, mid_ab)
        ]
