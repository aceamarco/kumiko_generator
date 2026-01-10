from PIL import Image

from config import GRID_WIDTH, GRID_HEIGHT, ORIENTATION, BACKGROUND_COLOR, TRIANGLE_BORDER_COLOR, \
    PROMINENT_COLOR_AMOUNT, EXCLUDE_BACKGROUND, FILE_PATH
from geometry.grid import HexagonGrid
from geometry.pattern.classifier import PatternClassifier
from image.sampler import ImageSampler
from image.utils import extract_prominent_colors, closest_palette_color
from rendering.svg_renderer import SVGRenderer

hex_grid = HexagonGrid(
    GRID_WIDTH,
    GRID_HEIGHT,
    30,
    orientation=ORIENTATION,
    triangle_fill=BACKGROUND_COLOR,
    triangle_stroke=TRIANGLE_BORDER_COLOR,
    offset_x=100,
    offset_y=100)

img = Image.open(FILE_PATH)
sampler = ImageSampler(img, hex_grid)

palette = extract_prominent_colors(img, num_colors=PROMINENT_COLOR_AMOUNT)

for c in palette:
    print("Extracted prominent color: ", f"rgb({c[0]},{c[1]},{c[2]})")


def render_svg(file_path: str, exclude_background: bool):
    renderer = SVGRenderer(background_color=BACKGROUND_COLOR)
    file_name = file_path.split(".")[0]

    for triangle in sampler.get_triangles():
        feature = sampler.sample(triangle)
        if feature:
            r, g, b = closest_palette_color(feature['avg_color_int'][:3], palette)

            rgb_string = f"rgb({r},{g},{b})"
            pattern_class = PatternClassifier.classify_feature(feature)
            triangle.stroke = TRIANGLE_BORDER_COLOR
            triangle.fill = BACKGROUND_COLOR
            triangle.pattern = pattern_class(stroke=rgb_string)
        renderer.add_triangle(triangle)

    x, y = renderer.get_center()
    renderer.adjust_center_with_padding(x - 12, y + 9)
    renderer.save(f"{file_name}.svg", False, exclude_background=exclude_background)
    renderer.save_summary(f"{file_name}_summary.svg")


render_svg(FILE_PATH, exclude_background=EXCLUDE_BACKGROUND)
