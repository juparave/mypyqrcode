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
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import argparse
import sys


def generate_qr_with_logo(data, logo_path=None, output_path="qr_code.png", style="rounded"):
    """
    Generate a QR code with optional logo embedding and custom styling.

    Args:
        data (str): The data to encode in the QR code
        logo_path (str, optional): Path to logo image to embed in QR code
        output_path (str): Path where the QR code image will be saved
        style (str): Style for the QR code modules ("circle", "gapped", "horizontal", 
                    "rounded", "square", "vertical")

    Returns:
        None
    """
    # Map style names to module drawers
    style_map = {
        "circle": CircleModuleDrawer(),
        "gapped": GappedSquareModuleDrawer(),
        "horizontal": HorizontalBarsDrawer(),
        "rounded": RoundedModuleDrawer(),
        "square": SquareModuleDrawer(),
        "vertical": VerticalBarsDrawer()
    }
    
    # Create QR code with high error correction for logo embedding
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Choose module drawer based on style
    module_drawer = style_map.get(style, RoundedModuleDrawer())
    
    # Generate the QR code image
    if logo_path:
        # With logo requires high error correction
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            embedded_image_path=logo_path
        )
    else:
        # Without logo - can use styling options
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=RadialGradiantColorMask()
        )

    # Save the image
    img.save(output_path)
    print(f"QR code saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate QR codes with optional logos")
    parser.add_argument("data", help="Data to encode in QR code")
    parser.add_argument("--logo", help="Path to logo image")
    parser.add_argument("--output", default="qr_code.png", help="Output file path")
    parser.add_argument("--style", choices=["circle", "gapped", "horizontal", "rounded", 
                                          "square", "vertical"], 
                       default="rounded", help="QR code module style")
    
    args = parser.parse_args()
    
    try:
        generate_qr_with_logo(args.data, args.logo, args.output, args.style)
    except Exception as e:
        print(f"Error generating QR code: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
