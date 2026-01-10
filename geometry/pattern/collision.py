from typing import List, Union

from geometry.pattern.pattern import Pattern
from geometry.primitives import Line, Arc


class CollisionPattern(Pattern):
    def _get_geometry(self, a, b, c) -> List[Union[Line, Arc]]:

        # Helper function to find a point along the line connecting p1 to p2
        def toward(p1, p2, factor):
            x1, y1 = p1
            x2, y2 = p2
            return (x1 + (x2 - x1) * factor, y1 + (y2 - y1) * factor)

        # 60% factor for collision lines
        f = 0.7

        # Each line starts at a vertex and points toward a point along the opposite side
        line_a = Line(a, toward(b, c, f))
        line_b = Line(b, toward(c, a, f))
        line_c = Line(c, toward(a, b, f))

        return [line_a, line_b, line_c]
