from geometry.pattern.pattern import Pattern
from geometry.primitives import QuadraticBezier


class ShippoPattern(Pattern):
    def get_material_cost(self) -> float:
        return 3.2

    def _get_geometry(self, a, b, c):
        # Compute centroid of triangle
        cx = (a[0] + b[0] + c[0]) / 3
        cy = (a[1] + b[1] + c[1]) / 3
        centroid = (cx, cy)

        # Create bezier curves from each vertex to the next, curving inward toward centroid
        mid_ab = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        mid_bc = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2)
        mid_ca = ((c[0] + a[0]) / 2, (c[1] + a[1]) / 2)

        cp_ab = Pattern.control_point(mid_ab, centroid)
        cp_bc = Pattern.control_point(mid_bc, centroid)
        cp_ca = Pattern.control_point(mid_ca, centroid)

        return [
            QuadraticBezier(start=a, control=cp_ab, end=b),
            QuadraticBezier(start=b, control=cp_bc, end=c),
            QuadraticBezier(start=c, control=cp_ca, end=a),
        ]