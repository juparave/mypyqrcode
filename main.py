import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import argparse
import sys


def generate_qr_with_logo(data, logo_path=None, output_path="qr_code.png"):
    """
    Generate a QR code with optional logo embedding.

    Args:
        data (str): The data to encode in the QR code
        logo_path (str, optional): Path to logo image to embed in QR code
        output_path (str): Path where the QR code image will be saved

    Returns:
        None
    """
    # Create QR code with high error correction for logo embedding
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate the QR code image
    if logo_path:
        # With logo requires high error correction
        img = qr.make_image(
            image_factory=StyledPilImage,
            embedded_image_path=logo_path
        )
    else:
        # Without logo - can use styling options
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
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
    
    args = parser.parse_args()
    
    try:
        generate_qr_with_logo(args.data, args.logo, args.output)
    except Exception as e:
        print(f"Error generating QR code: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
