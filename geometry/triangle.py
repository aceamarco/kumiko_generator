import math

from geometry.pattern.pattern import Pattern


class Triangle:
    def __init__(self, cx, cy, size, i, fill='none', stroke='black', hex_orientation='pointy', pattern: Pattern = None):
        self.cx = cx
        self.cy = cy
        self.size = size
        self.i = i
        self.fill = fill
        self.stroke = stroke
        self.hex_orientation = hex_orientation
        self.pattern = pattern

    def centroid(self):
        a, b, c = self.get_points()
        ax, ay = a
        bx, by = b
        cx, cy = c
        centroid_x = (ax + bx + cx) / 3
        centroid_y = (ay + by + cy) / 3
        return centroid_x, centroid_y

    @staticmethod
    def hex_corner(cx, cy, size, i, orientation):
        if orientation == 'pointy':
            angle_deg = 60 * i - 30
        elif orientation == 'flat':
            angle_deg = 60 * i
        else:
            raise ValueError("orientation must be 'pointy' or 'flat'")
        angle_rad = math.radians(angle_deg)
        return cx + size * math.cos(angle_rad), cy + size * math.sin(angle_rad)

    def get_points(self):
        a = self.hex_corner(self.cx, self.cy, self.size, self.i, self.hex_orientation)
        b = self.hex_corner(self.cx, self.cy, self.size, (self.i + 1) % 6, self.hex_orientation)
        return [a, b, (self.cx, self.cy)]

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return (self.cx == other.cx and
                self.cy == other.cy and
                self.size == other.size and
                self.i == other.i and
                self.fill == other.fill and
                self.stroke == other.stroke and
                self.hex_orientation == other.hex_orientation)

    def __hash__(self):
        return hash((self.cx, self.cy, self.size, self.i, self.fill, self.stroke, self.hex_orientation))
