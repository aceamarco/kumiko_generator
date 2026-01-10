# Kumiko Generator

This project generates **Kumiko-style geometric SVG panels** from an input image. It samples colors from the image, classifies local visual features, and maps them onto a hexagon-based triangle grid to produce printable or laser-cut–ready SVG files.

The output is especially suited for **3D printing, CNC, or laser cutting** decorative Kumiko panels, where each triangle can be rendered as a traditional Kumiko pattern.

---

## Features

* Hexagon-based triangle grid (flat or pointy orientation)
* Automatic extraction of prominent colors from an image
* Feature-based pattern classification per triangle
* SVG output optimized for fabrication
* Optional background exclusion for cleaner designs
* Summary SVG showing pattern usage

---

## Example Workflow

1. Choose an input image
2. Configure grid size, colors, and behavior in `config.py`
3. Run the generator
4. Import the generated SVG into your slicer / CAD / vector tool

---

## Installation

### Requirements

* Python 3.9+
* Installing required dependencies (Pillow, Scikit, Matplotlib etc)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```text
.
├── main.py                 # Entry point
├── config.py               # User configuration
├── geometry/
│   ├── grid.py             # Hexagon + triangle grid
│   └── pattern/
│       └── classifier.py   # Pattern selection logic
├── image/
│   ├── sampler.py          # Image-to-triangle sampling
│   └── utils.py            # Color extraction utilities
├── rendering/
│   └── svg_renderer.py     # SVG output
└── saturn.png              # Example input image
```

---

## Usage

### 1. Configure the Generator

All user-facing configuration lives in **`config.py`**.

#### Hexagon Orientation

```python
ORIENTATION = 'pointy'  # 'pointy' or 'flat'
```

Controls whether hexagons are point-up or flat-top.

---

#### Grid Resolution

```python
GRID_WIDTH = 30
GRID_HEIGHT = 30
```

These values control **both resolution and final panel size**.

* Keep width/height proportional to your image aspect ratio
* Increase both values to scale the design up while preserving detail

Example:

* `15 x 15` → small, low detail
* `30 x 30` → larger, more detailed
* `60 x 60` → very high detail (large SVG)

---

#### Input Image

```python
FILE_PATH = "saturn.png"
```

* PNG is fully supported
* Images with strong contrast work best

---

#### Color Extraction

```python
PROMINENT_COLOR_AMOUNT = 5
```

Controls how many dominant colors are extracted from the image.

Tips:

* If excluding background, add **+1** to your intended filament count
* If including background, set this equal to total colors desired

The script will print extracted colors:

```text
Extracted prominent color: rgb(123,45,67)
```

---

#### Background Handling

```python
BACKGROUND_COLOR = '#000000'
EXCLUDE_BACKGROUND = True
```

* `BACKGROUND_COLOR` sets the fill for unpatterned triangles
* `EXCLUDE_BACKGROUND=True` prevents patterns from being generated for background areas

Recommended:

* **Exclude background** for images with solid or empty backgrounds
* **Include background** for full-coverage images

---

#### Triangle Border Color

```python
TRIANGLE_BORDER_COLOR = '#683e07'
```

This color should match the filament or material used for the triangle outlines.

---

## Running the Generator

From the project root:

```bash
python main.py
```

This will generate:

* `input_name.svg` – full Kumiko panel
* `input_name_summary.svg` – overview of pattern usage

Example:

```text
saturn.svg
saturn_summary.svg
```

---

## Output Details

### Main SVG

* Each triangle is assigned a Kumiko pattern
* Stroke = `TRIANGLE_BORDER_COLOR`
* Pattern stroke = closest extracted palette color
* Background triangles optionally removed

### Summary SVG

* Shows how often each pattern was used
* Useful for balancing visual complexity

⚠️ **Important note about background patterns**

Even if `EXCLUDE_BACKGROUND = True`, the **summary SVG will still include pattern counts for background triangles**.

This means:

* The main SVG correctly excludes background patterns
* The summary SVG does **not** filter them out

When using the summary SVG, **manually ignore patterns that correspond to the background color** when evaluating pattern usage or planning filament counts.

---

## Fabrication Tips

* Count triangles to estimate print size
* Match triangle size to your nozzle / kerf
* Use single-color strokes for structural integrity
* Test-print a small section before committing

---

## Notes & Limitations

* Very large grids can produce heavy SVGs
* Non-PNG formats are untested
* Best results come from high-contrast images

---

## License

MIT (or your preferred license)

---

## Credits

Inspired by traditional Japanese Kumiko woodworking patterns.
