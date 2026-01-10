from geometry.pattern.pattern import Pattern
from geometry.primitives import QuadraticBezier


class SakuraPattern(Pattern):
    def get_material_cost(self) -> float:
        return 3.8

    def _get_geometry(self, a, b, c):
        # Compute centroid of triangle
        cx = (a[0] + b[0] + c[0]) / 3
        cy = (a[1] + b[1] + c[1]) / 3
        centroid = (cx, cy)

        def control_point(vertex, centroid, side=1, distance_factor=0.8, perpendicular_factor=0.4):
            # Vector from vertex to centroid
            vx = centroid[0] - vertex[0]
            vy = centroid[1] - vertex[1]

            # Offset perpendicular to the vector to create leaf curvature
            cp_x = vertex[0] + vx * distance_factor - side * vy * perpendicular_factor
            cp_y = vertex[1] + vy * distance_factor + side * vx * perpendicular_factor
            return (cp_x, cp_y)

        def endpoint(vertex, centroid, factor):
            # Interpolate along vertex->centroid
            return (vertex[0] + (centroid[0] - vertex[0]) * factor,
                    vertex[1] + (centroid[1] - vertex[1]) * factor)

        curves = []

        for vertex in [a, b, c]:
            end = endpoint(vertex, centroid, 0.95)
            # Two curves per vertex, opposite sides for leaf effect
            curves.append(QuadraticBezier(start=vertex, control=control_point(vertex, centroid, side=1), end=end))
            curves.append(QuadraticBezier(start=vertex, control=control_point(vertex, centroid, side=-1), end=end))

        return curves


