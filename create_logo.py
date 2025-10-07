"""
Generate L.I.F.E Platform Logo (216x216 PNG)
For Azure Marketplace Partner Center
Windows-compatible version
"""

import os
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow not installed!")
    print("Run: pip install Pillow")
    exit(1)


def create_life_logo():
    """Generate 216x216 logo for marketplace"""

    print("\n" + "=" * 60)
    print("Creating L.I.F.E Platform Logo...")
    print("=" * 60 + "\n")

    # Logo size (Partner Center requirement: 216x216 to 350x350)
    size = 280  # Using 280x280 for better quality
    img = Image.new("RGB", (size, size), color="white")
    draw = ImageDraw.Draw(img)

    # Azure blue circle background
    margin = 20
    draw.ellipse(
        [(margin, margin), (size - margin, size - margin)],
        fill="#0078D4",
        outline="#005A9E",
        width=4,
    )

    # Use default font (always works)
    try:
        # Try to use Arial
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 20)
    except:
        print("Using default font...")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Draw "L.I.F.E" text
    life_text = "L.I.F.E"
    life_bbox = draw.textbbox((0, 0), life_text, font=title_font)
    life_w = life_bbox[2] - life_bbox[0]
    life_h = life_bbox[3] - life_bbox[1]
    draw.text(
        ((size - life_w) // 2, (size - life_h) // 2 - 20),
        life_text,
        fill="white",
        font=title_font,
    )

    # Draw "Platform" text
    platform_text = "Platform"
    platform_bbox = draw.textbbox((0, 0), platform_text, font=subtitle_font)
    platform_w = platform_bbox[2] - platform_bbox[0]
    draw.text(
        ((size - platform_w) // 2, (size + life_h) // 2),
        platform_text,
        fill="white",
        font=subtitle_font,
    )

    return img


def main():
    """Main execution"""

    # Create output directory
    output_dir = "marketplace_assets"
    os.makedirs(output_dir, exist_ok=True)

    # Generate logo
    logo = create_life_logo()

    # Save logo
    logo_filename = "LIFE_Platform_Logo_280x280.png"
    logo_filepath = os.path.join(output_dir, logo_filename)
    logo.save(logo_filepath, "PNG", quality=95, optimize=True)

    # Also save as 216x216 (minimum size)
    logo_216 = logo.resize((216, 216), Image.Resampling.LANCZOS)
    logo_216_filename = "LIFE_Platform_Logo_216x216.png"
    logo_216_filepath = os.path.join(output_dir, logo_216_filename)
    logo_216.save(logo_216_filepath, "PNG", quality=95, optimize=True)

    # Get file sizes
    logo_size = os.path.getsize(logo_filepath) / 1024
    logo_216_size = os.path.getsize(logo_216_filepath) / 1024

    print(f"\n✅ SUCCESS! Logo created:")
    print(f"   📁 280x280: {logo_filepath} ({logo_size:.1f} KB)")
    print(f"   📁 216x216: {logo_216_filepath} ({logo_216_size:.1f} KB)")

    print("\n" + "=" * 60)
    print("UPLOAD TO PARTNER CENTER:")
    print("=" * 60)
    print("1. Go to Offer Listing section")
    print("2. Scroll to 'Logo' field")
    print("3. Upload: LIFE_Platform_Logo_280x280.png")
    print("4. Or use: LIFE_Platform_Logo_216x216.png (minimum size)")
    print("=" * 60 + "\n")

    return True


if __name__ == "__main__":
    success = main()
    input("\nPress Enter to close...")
