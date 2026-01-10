from geometry.pattern.pattern import Pattern
from geometry.primitives import QuadraticBezier


class YotsubaPattern(Pattern):
    def _get_geometry(self, a, b, c):
        ax, ay = a
        bx, by = b
        cx, cy = c

        centroid = (
            (ax + bx + cx) / 3,
            (ay + by + cy) / 3,
        )

        # Control points for leaf curves
        def ctrl_offset(p1, p2, offset=0.1):
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            return (mid_x, mid_y - offset), (mid_x, mid_y + offset)

        ctrl_ab1, ctrl_ab2 = ctrl_offset(a, b)
        ctrl_ac1, ctrl_ac2 = ctrl_offset(a, c)

        return [
            QuadraticBezier(start=a, control=ctrl_ab1, end=centroid),
            QuadraticBezier(start=a, control=ctrl_ab2, end=centroid),
            QuadraticBezier(start=a, control=ctrl_ac1, end=centroid),
            QuadraticBezier(start=a, control=ctrl_ac2, end=centroid),
        ]

