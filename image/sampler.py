import PIL
from PIL.Image import Image, Resampling
from matplotlib.path import Path
from skimage.color import rgb2gray, rgb2lab
from skimage.feature import local_binary_pattern
from skimage.filters import sobel
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.util import img_as_ubyte

from geometry.grid import HexagonGrid
from geometry.triangle import Triangle
import numpy as np


class ImageSampler:
    def __init__(self, image: Image, grid: HexagonGrid):
        self.container = (640, 360)
        self.grid = grid
        self.image = self._transform_image(image, grid)
        self.image_array = np.array(self.image)

        self.rgb_image_array = self.image_array[..., :3]
        self.gray_image = rgb2gray(self.rgb_image_array)
        self.lab_image = rgb2lab(self.rgb_image_array)

        # Precompute all necessary image features
        self.entropy_image = entropy(img_as_ubyte(self.gray_image), disk(3))
        self.gradient_magnitude = sobel(self.gray_image)
        self.lbp_image = local_binary_pattern(self.gray_image, P=8, R=1, method='uniform')

        self._mapped_triangles = self._map_triangles(self.image_array, grid)

    @staticmethod
    def unpremultiply_alpha(rgba):
        rgb = rgba[..., :3].astype(np.float32)
        alpha = rgba[..., 3:4].astype(np.float32) / 255.0
        with np.errstate(invalid='ignore', divide='ignore'):
            rgb_corrected = np.where(alpha > 0, rgb / alpha, 0)
        return np.clip(rgb_corrected, 0, 255).astype(np.uint8)

    def get_triangles(self):
        return self._mapped_triangles.keys()

    def get_mapped_triangles(self):
        return self._mapped_triangles.items()

    def get_vertices(self, triangle: Triangle):
        return self._mapped_triangles[triangle]

    def _map_triangles(self, image_array, grid: HexagonGrid):
        image_height, image_width = image_array.shape[:2]
        triangles = [triangle for hexagon in grid.hexagons for triangle in hexagon.triangles]
        return self.map_triangles_to_image_dict(triangles, image_width, image_height)

    def _transform_image(self, image: Image, grid: HexagonGrid):
        total_width_svg, total_height_svg = grid.calculate_svg_grid_size()
        container_width, container_height = self.container
        scale_x = container_width / total_width_svg
        scale_y = container_height / total_height_svg
        scale_factor = min(scale_x, scale_y)  # to fit entire grid without clipping

        target_img_width_px = total_width_svg * scale_factor
        target_img_height_px = total_height_svg * scale_factor
        return self.resize_and_pad(image, int(target_img_width_px), int(target_img_height_px))

    def sample(self, triangle: Triangle):
        height, width = self.image_array.shape[:2]
        vertices = np.array(self._mapped_triangles[triangle])
        xs, ys = vertices[:, 0], vertices[:, 1]
        min_x, max_x = max(int(xs.min()), 0), min(int(xs.max()) + 1, width)
        min_y, max_y = max(int(ys.min()), 0), min(int(ys.max()) + 1, height)

        X, Y = np.meshgrid(np.arange(min_x, max_x), np.arange(min_y, max_y))
        coords = np.vstack((X.ravel(), Y.ravel())).T

        path = Path(vertices)
        mask_flat = path.contains_points(coords)
        mask = mask_flat.reshape((max_y - min_y, max_x - min_x))

        slice_y = slice(min_y, max_y)
        slice_x = slice(min_x, max_x)

        # Exclude fully transparent pixels
        alpha_crop = self.image_array[slice_y, slice_x, 3]
        ALPHA_THRESHOLD = 10  # Adjust as needed (out of 255)
        mask &= (alpha_crop >= ALPHA_THRESHOLD)

        if not np.any(mask):
            return None

        rgb_crop = self.rgb_image_array[slice_y, slice_x]
        lab_crop = self.lab_image[slice_y, slice_x]
        entropy_crop = self.entropy_image[slice_y, slice_x]
        gradient_crop = self.gradient_magnitude[slice_y, slice_x]
        gray_crop = self.gray_image[slice_y, slice_x]
        lbp_crop = self.lbp_image[slice_y, slice_x]

        pixels = rgb_crop[mask]
        avg_color = pixels.mean(axis=0)

        lab_vals = lab_crop[mask]
        entropy_vals = entropy_crop[mask]
        gradient_vals = gradient_crop[mask]
        gray_vals = gray_crop[mask]
        lbp_vals = lbp_crop[mask]
        lbp_hist, _ = np.histogram(lbp_vals, bins=np.arange(11), density=True)

        return {
            'avg_color': avg_color,
            'avg_color_int': avg_color.astype(np.uint8),
            'pixel_count': len(pixels),
            'mask': mask,
            'bbox': (min_x, min_y, max_x, max_y),
            'mean_lab': lab_vals.mean(axis=0),
            'mean_entropy': entropy_vals.mean(),
            'mean_gradient': gradient_vals.mean(),
            'std_gray': gray_vals.std(),
            'lbp_hist': lbp_hist
        }

    @staticmethod
    def map_triangles_to_image_dict(triangles, image_width, image_height):
        all_points = np.array([pt for tri in triangles for pt in tri.get_points()])
        min_x, min_y = all_points.min(axis=0)
        max_x, max_y = all_points.max(axis=0)

        scale_x = image_width / (max_x - min_x)
        scale_y = image_height / (max_y - min_y)
        scale = min(scale_x, scale_y)

        def map_point(pt):
            x, y = pt
            return (x - min_x) * scale, (y - min_y) * scale

        return {tri: [map_point(pt) for pt in tri.get_points()] for tri in triangles}

    @staticmethod
    def resize_and_pad(image: Image, target_width: int, target_height: int) -> Image:
        img_ratio = image.width / image.height
        target_ratio = target_width / target_height

        if img_ratio > target_ratio:
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * img_ratio)

        resized = image.resize((new_width, new_height), Resampling.NEAREST)

        # Create transparent background
        new_image = PIL.Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        offset_x = (target_width - new_width) // 2
        offset_y = (target_height - new_height) // 2
        new_image.paste(resized, (offset_x, offset_y))
        return new_image

    @staticmethod
    def crop_to_non_transparent(image: Image) -> Image:
        alpha = image.getchannel('A')
        bbox = alpha.getbbox()  # Gets the bounding box of non-transparent pixels
        if bbox:
            return image.crop(bbox)
        return image  # If completely transparent, return as-is