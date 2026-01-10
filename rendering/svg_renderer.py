import importlib
from collections import defaultdict
from pathlib import Path

from geometry.pattern.pattern import Pattern
from geometry.primitives import Line, QuadraticBezier
from geometry.triangle import Triangle


class SVGRenderer:
    def __init__(self, background_color: str):
        self.elements = []
        self.min_x = float('inf')
        self.min_y = float('inf')
        self.max_x = float('-inf')
        self.max_y = float('-inf')
        self.dx = None
        self.dy = None
        self.pattern_counter = defaultdict(int)
        self.background_color = background_color

        print(self.background_color)

    def add(self, element_svg: str):
        self.elements.append(element_svg)

    def update_bounds(self, x, y):
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)

    def add_triangle(self, triangle: Triangle):
        points = triangle.get_points()
        point_str = ' '.join(f'{x},{y}' for x, y in points)

        svg = f'<polygon points="{point_str}" fill="{triangle.fill}" stroke="{triangle.stroke}" />'
        # svg = ""
        if triangle.pattern:
            for shape in triangle.pattern.get_geometry(*points):
                svg += self.render_shape(shape, triangle.pattern.stroke, triangle.pattern.stroke_width)

            key = (triangle.pattern.__class__, triangle.pattern.stroke)
            self.pattern_counter[key] += 1

        self.add(svg)

    def render_shape(self, shape, stroke, stroke_width):
        if isinstance(shape, Line):
            return self.render_line_svg(shape, stroke, stroke_width)
        elif isinstance(shape, QuadraticBezier):
            return self.render_bezier_svg(shape, stroke, stroke_width)

    def render_line_svg(self, line: Line, stroke, stroke_width):
        x1, y1 = line.start
        x2, y2 = line.end
        self.update_bounds(x1, y1)
        self.update_bounds(x2, y2)

        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}" />'

    def render_bezier_svg(self, bez: QuadraticBezier, stroke, stroke_width):
        x0, y0 = bez.start
        cx, cy = bez.control
        x1, y1 = bez.end
        for x, y in [bez.start, bez.control, bez.end]:
            self.update_bounds(x, y)
        return f'<path d="M {x0} {y0} Q {cx} {cy} {x1} {y1}" stroke="{stroke}" stroke-width="{stroke_width}" fill="none" />'

    def width(self):
        return self.max_x - self.min_x

    def height(self):
        return self.max_y - self.min_y

    def adjust_center(self, target_cx: float, target_cy: float):
        current_cx, current_cy = self.get_center()
        dx = target_cx - current_cx
        dy = target_cy - current_cy

        # Expand the bounding box to shift the center
        self.min_x -= dx
        self.max_x -= dx
        self.min_y -= dy
        self.max_y -= dy

    def get_bounds(self):
        return self.min_x, self.min_y, self.max_x, self.max_y

    def get_center(self):
        cx = (self.min_x + self.max_x) / 2
        cy = (self.min_y + self.max_y) / 2
        return cx, cy

    def adjust_center_with_padding(self, target_cx: float, target_cy: float):
        current_cx, current_cy = self.get_center()
        dx = target_cx - current_cx
        dy = target_cy - current_cy

        # Shift bounds to center around the target
        self.min_x -= dx
        self.max_x -= dx
        self.min_y -= dy
        self.max_y -= dy

        # Now ensure that the canvas is centered around target_cx, target_cy
        half_width = max(abs(self.max_x - target_cx), abs(self.min_x - target_cx))
        half_height = max(abs(self.max_y - target_cy), abs(self.min_y - target_cy))

        self.min_x = target_cx - half_width
        self.max_x = target_cx + half_width
        self.min_y = target_cy - half_height
        self.max_y = target_cy + half_height

    def render(self, debug, exclude_background):
        width = self.width()
        height = self.height()
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" '
               f'width="{width}" height="{height}" '
               f'viewBox="{self.min_x} {self.min_y} {width} {height}">']

        if exclude_background:
            unique_color_strings = set(map(lambda x:x[1], self.pattern_counter.keys()))
            color_dict = {}
            for unique_color_string in unique_color_strings:
                keys = []
                for key in self.pattern_counter.keys():
                    if key[1] == unique_color_string:
                        keys.append(key)
                total = 0
                for key in keys:
                    total += self.pattern_counter.get(key)

                color_dict[unique_color_string] = total

            sorted_dict = sorted(color_dict.items(), key=lambda x:x[1], reverse=True)
            exlude_color = sorted_dict[0][0]

            elements = []
            for element in self.elements:
                if exlude_color in element:
                    new_element = element.replace(exlude_color, self.background_color)
                    elements.append(new_element)
                else:
                    elements.append(element)
            svg.extend(elements)

        else:
            svg.extend(self.elements)

        if debug:
            center_x = (self.min_x + self.max_x) / 2
            center_y = (self.min_y + self.max_y) / 2
            svg.append(f'<line x1="{self.min_x}" y1="{center_y}" x2="{self.max_x}" y2="{center_y}" '
                       f'stroke="red" stroke-width="0.5" stroke-dasharray="4" />')
            svg.append(f'<line x1="{center_x}" y1="{self.min_y}" x2="{center_x}" y2="{self.max_y}" '
                       f'stroke="red" stroke-width="0.5" stroke-dasharray="4" />')

        svg.append('</svg>')
        return "\n".join(svg)

    def save(self, filename="output.svg", debug=False, exclude_background=False):
        Path(filename).write_text(self.render(debug, exclude_background), encoding="utf-8")
        print(f"✅ SVG saved to {filename}")

    def render_summary(self, tile_size=50, padding=40, font_size=12, cols=5, exclude_colors=None):
        """
        Render a summary of all unique pattern+color combinations,
        using the real pattern geometry.
        """
        if exclude_colors is None:
           exclude_colors = []

        items = list(self.pattern_counter.items())
        items = sorted(items, key=lambda x: x[0][1])

        num_items = len(items)
        rows = (num_items + cols - 1) // cols

        width = cols * (tile_size + padding)
        height = rows * (tile_size + padding + font_size + 5)

        svg_content = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']

        for idx, ((pattern_cls, color), count) in enumerate(items):
            if color in exclude_colors:
                continue

            row = idx // cols
            col = idx % cols
            x_offset = col * (tile_size + padding)
            y_offset = row * (tile_size + padding + font_size + 5)

            # Create points for the triangle tile and apply offset
            p1 = (0 + x_offset, 0 + y_offset)
            p2 = (tile_size + x_offset, 0 + y_offset)
            p3 = (tile_size / 2 + x_offset, tile_size * 0.866 + y_offset)
            points = [p1, p2, p3]

            points_str = ' '.join(f'{x},{y}' for x, y in points)
            svg = f'<polygon points="{points_str}" fill="none" stroke="rgb(104, 62, 7)" stroke-width="1"/>'

            # Instantiate the actual pattern class
            # Here we assume pattern_cls_name exists in globals()
            pattern = pattern_cls(stroke=color)
            # Render pattern geometry inside tile
            for shape in pattern.get_geometry(*points):
                svg += self.render_shape(shape, pattern.stroke, "2")

            # Draw triangle outline around pattern

            svg_content.append(svg)

            # Add label below
            svg_content.append(
                f'<text x="{x_offset + tile_size / 2}" y="{y_offset + tile_size + font_size}" '
                f'font-size="{font_size}" text-anchor="middle" fill="black">{count}</text>'
                f'<text x="{x_offset + tile_size / 2}" y="{(y_offset + font_size * 2) + tile_size}" '
                f'font-size="{font_size}" text-anchor="middle" fill="{color}">{color}</text>'
                f'<text x="{x_offset + tile_size / 2}" y="{(y_offset + font_size * 3) + tile_size}" '
                f'font-size="{font_size}" text-anchor="middle" fill="{color}">{count * pattern.get_material_cost()}g</text>'
            )



        svg_content.append('</svg>')
        return "\n".join(svg_content)

    @staticmethod
    def get_subclass_by_name(parent, name):
        for subclass in parent.__subclasses__():
            if subclass.__name__ == name:
                return subclass
        return None

    def save_summary(self, filename="summary.svg", tile_size=50, padding=40, font_size=12, cols=5, exclude_colors=None):
        Path(filename).write_text(self.render_summary(tile_size, padding, font_size, cols, exclude_colors), encoding="utf-8")
        print(f"✅ Summary SVG saved to {filename}")
