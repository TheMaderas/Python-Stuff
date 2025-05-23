"""
Interactive QR Code maker.
Simply enter text or a URL, and get a stylish QR code.
"""
import qrcode
from qrcode.image.svg import SvgImage
import os

try:
    import qrcode
except ImportError:
    print("Error: 'qrcode' package not found. Run 'pip3 install qrcode pillow'.")
    exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: 'Pillow' package not found. Run 'pip3 install pillow'.")
    exit(1)

def generate_qrcode(data, output_name=None, file_format="svg", scale=8, quiet_zone=4):
    """
    Generates a QR code with the specified options.
    
    Args:
        data (str): Data to be encoded in the QR Code
        output_name (str): Output filename (without extension)
        file_format (str): File format (svg or png)
        scale (int): QR Code scale
        quiet_zone (int): Size of the quiet zone around the QR Code
        
    Returns:
        str: Path to the generated file
    """
    # Determine output filename
    if not output_name:
        if data.startswith(('http://', 'https://')):
            from urllib.parse import urlparse
            domain = urlparse(data).netloc
            output_name = domain.replace('.', '_')
        else:
            output_name = 'qrcode'
    filename = f"{output_name}.{file_format}"

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=scale,
        border=quiet_zone
    )
    qr.add_data(data)
    qr.make(fit=True)

    fmt = file_format.lower()
    if fmt == 'svg':
        img = qr.make_image(image_factory=SvgImage, fill_color="#003366", back_color="white")
        with open(filename, 'wb') as f:
            img.save(f)
    elif fmt == 'png':
        img = qr.make_image(fill_color="#003366", back_color="white").convert('RGB')
        img.save(filename)
    else:
        raise ValueError(f"Unsupported format: {file_format}")

    return filename

def main():
    default_link = "https://www.github.com/themaderas"
    default_format = "svg"
    default_scale = 8
    default_border = 4

    print("\nWelcome to the QR Code Generator!")
    print(f"(Press Enter to use defaults: URL='{default_link}', format={default_format}, size={default_scale}, border={default_border})\n")

    data = input("Enter text or URL: ").strip()
    if not data:
        data = default_link

    fmt = input(f"Format [svg/png] (default {default_format}): ").strip().lower()
    if fmt not in ('svg', 'png'):
        fmt = default_format

    scale_input = input(f"Box size (scale) (default {default_scale}): ").strip()
    try:
        scale = int(scale_input)
    except ValueError:
        scale = default_scale

    border_input = input(f"Border size (quiet zone) (default {default_border}): ").strip()
    try:
        quiet_zone = int(border_input)
    except ValueError:
        quiet_zone = default_border

    print(f"\nGenerating QR code for: {data}")
    try:
        filename = generate_qrcode(data, None, fmt, scale, quiet_zone)
        print(f"✔ Saved: {filename}")
        print(f"→ Location: {os.path.abspath(filename)}")
    except Exception as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    main()
