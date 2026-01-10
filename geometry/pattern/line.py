from geometry.pattern.pattern import Pattern


class LinePattern(Pattern):
    def _to_svg(self, a, b, c):
        # Assume triangle points are a, b, c
        # Let's draw a line from midpoint of base (a, b) to top (c)

        mid_base_x = (a[0] + b[0]) / 2
        mid_base_y = (a[1] + b[1]) / 2

        tip_x, tip_y = c

        return f'<line x1="{mid_base_x}" y1="{mid_base_y}" x2="{tip_x}" y2="{tip_y}" stroke="{self.stroke}" stroke-width="{self.stroke_width}" />'
