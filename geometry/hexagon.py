
from geometry.pattern.asanoha import AsanohaPattern
from geometry.triangle import Triangle


class Hexagon:
    def __init__(self, cx, cy, size, orientation='pointy', triangle_fill='none', triangle_stroke='black'):
        self.cx = cx
        self.cy = cy
        self.size = size
        self.orientation = orientation  # 'pointy' or 'flat'
        self.triangles = []
        self.triangle_fill = triangle_fill
        self.triangle_stroke = triangle_stroke
        self._create_triangles()

    def wrap_offset(self, input_num, limit, offset):
        return (input_num + offset) % limit

    def _create_triangles(self):
        self.triangles.clear()
        for i in range(6):
            self.triangles.append(
                Triangle(
                    self.cx,
                    self.cy,
                    self.size,
                    self.wrap_offset(i, 6, 3),
                    fill=self.triangle_fill,
                    stroke=self.triangle_stroke,
                    hex_orientation=self.orientation,
                    #pattern=AsanohaPattern(stroke=self.triangle_stroke)
                )
            )

    def to_svg(self):
        # Return SVG of all 6 triangles
        return '\n'.join(t.to_svg() for t in self.triangles)

    def triangles_svg(self):
        return '\n'.join(t.to_svg() for t in self.triangles)