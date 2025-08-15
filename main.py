import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask
)
from PIL import Image, ImageDraw
import argparse
import sys


def parse_color(color_str):
    """
    Parse a color string in hex format (#RRGGBB) to RGB tuple.
    
    Args:
        color_str (str): Color in hex format
        
    Returns:
        tuple: RGB tuple (r, g, b)
    """
    if color_str.startswith('#'):
        color_str = color_str[1:]
    return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))


def overlay_logo_on_qr(qr_img, logo_path, logo_gap=0):
    """
    Overlay a logo image onto the center of a QR code with optional gap.
    
    Args:
        qr_img (PIL.Image): QR code image
        logo_path (str): Path to logo image
        logo_gap (int): Number of pixels gap between logo and QR code data
        
    Returns:
        PIL.Image: QR code with logo overlaid
    """
    # Open the logo image
    logo = Image.open(logo_path)
    
    # Calculate the size of the logo (typically 10-20% of QR code size)
    qr_width, qr_height = qr_img.size
    logo_size = min(qr_width, qr_height) // 4  # 25% of QR code size
    
    # Reduce logo size further if logo_gap is specified
    if logo_gap > 0:
        # Reduce logo size to account for the gap
        logo_size = logo_size - (logo_gap * 2)
    
    # Resize logo while maintaining aspect ratio
    logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
    
    # Calculate position to center the logo
    logo_width, logo_height = logo.size
    x = (qr_width - logo_width) // 2
    y = (qr_height - logo_height) // 2
    
    # Create a copy of the QR code to avoid modifying the original
    qr_with_logo = qr_img.copy()


    # Draw a white border (rectangle) around the logo area if logo_gap > 0
    if logo_gap > 0:
        border_rect = [
            x - logo_gap,
            y - logo_gap,
            x + logo_width + logo_gap,
            y + logo_height + logo_gap
        ]
        draw = ImageDraw.Draw(qr_with_logo)
        draw.rectangle(border_rect, fill="white")

    # Paste the logo onto the QR code (after gap is created)
    if logo.mode == 'RGBA':
        qr_with_logo.paste(logo, (x, y), logo)
    else:
        qr_with_logo.paste(logo, (x, y))

    return qr_with_logo


def generate_qr_with_logo(data, logo_path=None, logo_gap=0, output_path="qr_code.png", style="rounded", 
                         gradient_type="radial", gradient_color="#000000", size="normal"):
    """
    Generate a QR code with optional logo embedding and custom styling.

    Args:
        data (str): The data to encode in the QR code
        logo_path (str, optional): Path to logo image to embed in QR code
        logo_gap (int): Number of pixels gap between logo and QR code data
        output_path (str): Path where the QR code image will be saved
        style (str): Style for the QR code modules ("circle", "gapped", "horizontal", 
                    "rounded", "square", "vertical")
        gradient_type (str): Type of gradient ("radial", "square", "horizontal", "vertical")
        gradient_color (str): Color for gradient in hex format (#RRGGBB)
        size (str): Size of the QR code ("normal", "large", "xlarge")

    Returns:
        None
    """
    # Map size options to box_size values
    size_map = {
        "normal": 10,
        "large": 15,
        "xlarge": 20
    }
    
    # Get box_size based on size parameter
    box_size = size_map.get(size, 10)
    
    # Map style names to module drawers (with size-aware rounded style)
    style_map = {
        "circle": CircleModuleDrawer(),
        "gapped": GappedSquareModuleDrawer(),
        "horizontal": HorizontalBarsDrawer(),
        "rounded": RoundedModuleDrawer(radius_ratio=0.5),  # Adjust radius based on module size
        "square": SquareModuleDrawer(),
        "vertical": VerticalBarsDrawer()
    }
    
    # Map gradient types to color masks
    gradient_map = {
        "radial": RadialGradiantColorMask,
        "square": SquareGradiantColorMask,
        "horizontal": HorizontalGradiantColorMask,
        "vertical": VerticalGradiantColorMask
    }
    
    # Create QR code with high error correction for logo embedding
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Choose module drawer based on style
    module_drawer = style_map.get(style, RoundedModuleDrawer())
    
    # Parse gradient color
    try:
        color_rgb = parse_color(gradient_color)
    except (ValueError, IndexError):
        print(f"Invalid color format: {gradient_color}. Using default black (#000000)")
        color_rgb = (0, 0, 0)
    
    # Generate the QR code image with gradient
    # Choose color mask based on gradient type
    color_mask_class = gradient_map.get(gradient_type, RadialGradiantColorMask)
    
    # Create color mask with appropriate parameters for each type
    if gradient_type in ["radial", "square"]:
        color_mask = color_mask_class(
            back_color=(255, 255, 255),
            center_color=(0, 0, 0),
            edge_color=color_rgb
        )
    elif gradient_type == "horizontal":
        color_mask = color_mask_class(
            back_color=(255, 255, 255),
            left_color=(0, 0, 0),
            right_color=color_rgb
        )
    elif gradient_type == "vertical":
        color_mask = color_mask_class(
            back_color=(255, 255, 255),
            top_color=(0, 0, 0),
            bottom_color=color_rgb
        )
    else:
        # Default to radial gradient
        color_mask = color_mask_class(
            back_color=(255, 255, 255),
            center_color=(0, 0, 0),
            edge_color=color_rgb
        )
    
    # Generate QR code with gradient
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        color_mask=color_mask
    )
    
    # If logo is specified, overlay it manually
    if logo_path:
        img = overlay_logo_on_qr(img, logo_path, logo_gap)

    # Save the image
    img.save(output_path)
    print(f"QR code saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate QR codes with optional logos")
    parser.add_argument("data", help="Data to encode in QR code")
    parser.add_argument("--logo", help="Path to logo image")
    parser.add_argument("--logo-gap", type=int, default=0, help="Gap between logo and QR code data in pixels")
    parser.add_argument("--output", default="qr_code.png", help="Output file path")
    parser.add_argument("--style", choices=["circle", "gapped", "horizontal", "rounded", 
                                          "square", "vertical"], 
                       default="rounded", help="QR code module style")
    parser.add_argument("--gradient-type", choices=["radial", "square", "horizontal", "vertical"],
                       default="radial", help="Gradient type for QR code")
    parser.add_argument("--gradient-color", default="#000000", 
                       help="Gradient color in hex format (#RRGGBB)")
    parser.add_argument("--size", choices=["normal", "large", "xlarge"],
                       default="normal", help="Size of the QR code")
    
    args = parser.parse_args()
    
    try:
        generate_qr_with_logo(
            args.data, 
            args.logo, 
            args.logo_gap,
            args.output, 
            args.style,
            args.gradient_type,
            args.gradient_color,
            args.size
        )
    except Exception as e:
        print(f"Error generating QR code: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()