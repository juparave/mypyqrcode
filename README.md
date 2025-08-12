# mypyqrcode

A Python project for generating custom QR codes with logos using astral and uv/uvx.

## Features

- Generate QR codes with custom styling
- Embed logos in QR codes with gradient backgrounds
- Add gaps around logos for cleaner appearance
- Command-line interface for easy usage
- Multiple module styles (circles, rounded squares, horizontal/vertical bars, etc.)
- Gradient color options with customizable colors

## Installation

```bash
# Install dependencies
uv pip install qrcode[pil] astral

# Or install in development mode
uv pip install -e .
```

## Usage

### Command Line

```bash
# Generate a basic QR code with rounded modules (default)
python main.py "https://example.com" --output example_qr.png

# Generate a QR code with circle modules
python main.py "https://example.com" --style circle --output circle_qr.png

# Generate a QR code with horizontal bar modules
python main.py "https://example.com" --style horizontal --output horizontal_qr.png

# Generate a QR code with a red gradient
python main.py "https://example.com" --gradient-color "#FF0000" --output red_gradient_qr.png

# Generate a QR code with horizontal gradient from black to blue
python main.py "https://example.com" --gradient-type horizontal --gradient-color "#0000FF" --output horizontal_blue_qr.png

# Generate a QR code with a logo
python main.py "https://example.com" --logo logo.png --output qr_with_logo.png

# Generate a QR code with a logo and 5-pixel gap
python main.py "https://example.com" --logo logo.png --logo-gap 5 --output qr_with_logo_and_gap.png

# Generate a QR code with a logo, blue gradient background, and 3-pixel gap
python main.py "https://example.com" --logo logo.png --logo-gap 3 --gradient-color "#0000FF" --output qr_with_logo_gradient_and_gap.png
```

### Style Options

- `circle` - Circular modules
- `gapped` - Squares with gaps between modules
- `horizontal` - Horizontal bars
- `rounded` - Squares with rounded corners (default)
- `square` - Traditional square modules
- `vertical` - Vertical bars

### Gradient Types

- `radial` - Radial gradient from center to edges (default)
- `square` - Square gradient from center to edges
- `horizontal` - Horizontal gradient from left to right
- `vertical` - Vertical gradient from top to bottom

### Gradient Colors

Colors are specified in hex format (#RRGGBB). Examples:
- `#FF0000` - Red
- `#00FF00` - Green
- `#0000FF` - Blue
- `#FFFF00` - Yellow

### Logo Gap

The `--logo-gap` parameter specifies the number of pixels of whitespace to leave around the logo, creating a cleaner appearance by preventing the logo from overlapping with QR code data dots.

### Python API

```python
from main import generate_qr_with_logo

# Generate QR code with embedded logo and gap
generate_qr_with_logo("https://example.com", "logo.png", logo_gap=5, output_path="output.png")

# Generate QR code with circle modules
generate_qr_with_logo("https://example.com", style="circle", output_path="circle_qr.png")

# Generate QR code with red radial gradient
generate_qr_with_logo("https://example.com", gradient_color="#FF0000", output_path="red_qr.png")

# Generate QR code with horizontal blue gradient, logo, and gap
generate_qr_with_logo("https://example.com", logo_path="logo.png", logo_gap=3,
                     gradient_type="horizontal", gradient_color="#0000FF", 
                     output_path="blue_gradient_qr.png")
```

## Development

### Linting

```bash
ruff check .
ruff format .
```

### Testing

```bash
pytest
```

## Project Structure

- `main.py` - Main module with QR code generation functions
- `CRUSH.md` - Crush agent configuration and commands
- `pyproject.toml` - Project metadata and dependencies

## Dependencies

- `qrcode` - Core QR code generation library
- `Pillow` - Image processing library
- `astral` - Astral library (for potential future use)