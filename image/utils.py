import numpy as np
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans


def closest_palette_color(avg_color, palette):
    """
    avg_color: tuple/list of (R, G, B)
    palette: list of (R, G, B)

    Returns the palette color closest to avg_color.
    """
    avg = np.array(avg_color)
    palette_arr = np.array(palette)

    distances = np.linalg.norm(palette_arr - avg, axis=1)
    closest_index = distances.argmin()

    return tuple(palette_arr[closest_index].astype(int))


def extract_prominent_colors(image: Image, num_colors=8):
    img = image.convert('RGB')
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    return [tuple(color) for color in colors]


def extract_prominent_colors_read(image_path, num_colors=8, resize_to=(100, 100)):
    """
    Extract prominent colors from an image using k-means clustering after downscaling.

    Args:
        image_path (str): Path to the image file.
        num_colors (int): Number of colors to extract.
        resize_to (tuple): Size to downscale the image to (width, height).

    Returns:
        List of (R, G, B) tuples representing prominent colors.
    """
    img = Image.open(image_path)
    img = img.convert('RGB')
    img = img.resize(resize_to, Image.LANCZOS)  # High quality downscale

    pixels = np.array(img).reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    return [tuple(color) for color in colors]



def visualize_palette(colors, swatch_size=50, margin=5):
    """
    Creates a palette image visualizing the input colors.

    Args:
        colors (list of tuples): List of (R, G, B) colors.
        swatch_size (int): Size of each color square.
        margin (int): Space between color swatches.

    Returns:
        PIL.Image.Image: Image visualizing the palette.
    """
    num_colors = len(colors)
    width = num_colors * swatch_size + (num_colors + 1) * margin
    height = swatch_size + 2 * margin

    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    for i, color in enumerate(colors):
        x0 = margin + i * (swatch_size + margin)
        y0 = margin
        x1 = x0 + swatch_size
        y1 = y0 + swatch_size
        draw.rectangle([x0, y0, x1, y1], fill=color)

    return img


