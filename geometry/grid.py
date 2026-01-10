from enum import Enum
import math

from geometry.hexagon import Hexagon
from geometry.triangle import Triangle


class TriangleGrid:
    def __init__(self, cols, rows, triangles):
        self.cols = cols
        self.rows = rows
        self._triangles = triangles

    def get(self, col, row) -> Triangle | None:
        try:
            return self._triangles[col][row]
        except IndexError:
            return None


class HexagonGrid:
    def __init__(self, cols, rows, size, orientation='pointy', triangle_fill='none', triangle_stroke='black',
                 offset_x=0, offset_y=0):
        self.cols = cols
        self.rows = rows
        self.size = size
        self.orientation = orientation
        self.triangle_fill = triangle_fill
        self.triangle_stroke = triangle_stroke
        self.offset_x = offset_x
        self.offset_y = offset_y

        if orientation == 'pointy':
            self.h_spacing = size * 3 / 2
            self.v_spacing = size * math.sqrt(3)
        elif orientation == 'flat':
            self.h_spacing = size * math.sqrt(3)
            self.v_spacing = size * 3 / 2
        else:
            raise ValueError("orientation must be 'pointy' or 'flat'")

        self.hexagons = self._create_grid()

    def calculate_svg_grid_size(self):
        if self.orientation == 'pointy':
            return self.calculate_svg_grid_size_pointy()
        elif self.orientation == 'flat':
            return self.calculate_svg_grid_size_flat()

    def calculate_svg_grid_size_flat(self):
        hex_width = 2 * self.size
        hex_height = math.sqrt(3) * self.size

        total_width = hex_width * (self.cols * 0.75 + 0.25)
        total_height = hex_height * (self.rows + 0.5)
        return total_width, total_height

    def calculate_svg_grid_size_pointy(self):
        hex_height = self.size * 2
        hex_width = math.sqrt(3) * self.size

        # vertical spacing between hex centers
        vert_spacing = 0.75 * hex_height  # = size * 1.5

        total_width = hex_width * (self.cols + 0.5)  # add 0.5 for offset in even/odd rows
        total_height = vert_spacing * (self.rows - 1) + hex_height

        return total_width, total_height

    def get_hex(self, col, row):
        return self.hexagons[row * self.cols + col]

    def get_triangle_grid(self) -> TriangleGrid:
        if self.orientation == "pointy":
            return self._get_triangle_grid_pointy()
        else:
            return self._get_triangle_grid_flat()

    def _get_triangle_grid_flat(self) -> TriangleGrid:
        triangles = []
        tri_col = 0
        # For flat hex grid, width is primary axis, so iterate cols first
        for hex_col in range(self.cols):
            for attempt in range(3):
                idx = tri_col + attempt

                # Ensure enough rows in triangles list
                while len(triangles) <= idx:
                    triangles.append([])

                # Add padding None at the top edge for odd columns to keep alignment
                if hex_col % 2 != 0:
                    triangles[idx].append(None)

                for hex_row in range(self.rows):
                    hexagon = self.get_hex(hex_col, hex_row)

                    # Append triangles pairs according to attempt
                    if attempt == 0:
                        triangles[idx].append(hexagon.triangles[0])
                        triangles[idx].append(hexagon.triangles[5])
                    elif attempt == 1:
                        triangles[idx].append(hexagon.triangles[1])
                        triangles[idx].append(hexagon.triangles[4])
                    else:  # attempt == 2
                        triangles[idx].append(hexagon.triangles[2])
                        triangles[idx].append(hexagon.triangles[3])

                # Add padding None at bottom edge for odd columns (matching top padding length)
                if hex_col % 2 != 0:
                    triangles[idx].append(None)

            tri_col += 3

        total_rows = len(triangles)
        total_cols = max(len(row) for row in triangles) if triangles else 0
        return TriangleGrid(total_rows, total_cols, triangles)

    def _get_triangle_grid_pointy(self) -> TriangleGrid:
        triangles = []
        tri_col = 0
        # For pointy hex grid, height (rows) is primary axis, so iterate rows first
        for hex_row in range(self.rows):
            for attempt in range(3):
                idx = tri_col + attempt

                # Ensure enough rows in triangles list
                while len(triangles) <= idx:
                    triangles.append([])

                # Add padding None at left edge for odd rows to keep alignment
                if hex_row % 2 != 0:
                    triangles[idx].append(None)

                for hex_col in range(self.cols):
                    hexagon = self.get_hex(hex_col, hex_row)

                    if attempt == 0:
                        triangles[idx].append(hexagon.triangles[1])
                        triangles[idx].append(hexagon.triangles[2])
                    elif attempt == 1:
                        triangles[idx].append(hexagon.triangles[0])
                        triangles[idx].append(hexagon.triangles[3])
                    else:  # attempt == 2
                        triangles[idx].append(hexagon.triangles[5])
                        triangles[idx].append(hexagon.triangles[4])

                # Add padding None at right edge for odd rows (matching left padding length)
                if hex_row % 2 != 0:
                    triangles[idx].append(None)

            tri_col += 3

        total_rows = len(triangles)
        total_cols = max(len(row) for row in triangles) if triangles else 0
        return TriangleGrid(total_rows, total_cols, triangles)

    def _create_grid(self):
        hexes = []

        size = self.size
        sqrt3 = math.sqrt(3)

        if self.orientation == 'flat':
            dx = 1.5 * size
            dy = sqrt3 * size
            for row in range(self.rows):
                for col in range(self.cols):
                    x = col * dx + self.offset_x
                    y = row * dy + (col % 2) * (dy / 2) + self.offset_y
                    hexes.append(Hexagon(x, y, size,
                                         orientation=self.orientation,
                                         triangle_fill=self.triangle_fill,
                                         triangle_stroke=self.triangle_stroke))

        elif self.orientation == 'pointy':
            dx = sqrt3 * size
            dy = 1.5 * size
            for row in range(self.rows):
                for col in range(self.cols):
                    x = col * dx + (row % 2) * (dx / 2) + self.offset_x
                    y = row * dy + self.offset_y
                    hexes.append(Hexagon(x, y, size,
                                         orientation=self.orientation,
                                         triangle_fill=self.triangle_fill,
                                         triangle_stroke=self.triangle_stroke))

        return hexes
