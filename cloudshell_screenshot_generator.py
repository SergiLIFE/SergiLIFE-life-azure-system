#!/usr/bin/env python3
"""
L.I.F.E Platform - Cloud Shell Screenshot Generator
Creates professional 1280x720 screenshots in Azure Cloud Shell environment
Compatible with Linux/Cloud Shell (no Windows paths)
"""

import os
import sys
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ ERROR: Pillow not installed!")
    print("Run this command first: pip install --user Pillow")
    print("Or run: bash cloudshell_setup.sh")
    sys.exit(1)


def create_marketplace_screenshot():
    """Generate professional marketplace screenshot (1280x720)"""

    print("Creating L.I.F.E Platform marketplace screenshot...")

    # Image dimensions (Partner Center requirement)
    width, height = 1280, 720

    # Create image with Azure blue gradient background
    img = Image.new("RGB", (width, height), color="#0078D4")
    draw = ImageDraw.Draw(img)

    # Create gradient effect (darker at bottom)
    for y in range(height):
        darkness = int(255 * (1 - y / height * 0.3))
        color = (0, int(120 * darkness / 255), int(212 * darkness / 255))
        draw.rectangle([(0, y), (width, y + 1)], fill=color)

    # White content area with border
    margin = 80
    draw.rectangle(
        [(margin, margin), (width - margin, height - margin)],
        fill="white",
        outline="#0078D4",
        width=4,
    )

    # Use default font (works in Cloud Shell without font files)
    try:
        # Try system fonts (might work in Cloud Shell)
        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60
        )
        subtitle_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30
        )
        metric_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48
        )
        label_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24
        )
    except:
        print("⚠️  Using default font (no TrueType fonts found)")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        metric_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    # Title
    title = "L.I.F.E Platform"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 110), title, fill="#0078D4", font=title_font)

    # Subtitle
    subtitle = "Neuroadaptive Learning System"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(
        ((width - subtitle_w) // 2, 190), subtitle, fill="#505050", font=subtitle_font
    )

    # Key metrics section
    metrics_y = 280

    metrics = [
        {"value": "95.8%", "label": "Neural Processing Accuracy", "x": 180},
        {"value": "0.42ms", "label": "Processing Latency", "x": 520},
        {"value": "880x", "label": "Faster Than Competitors", "x": 860},
    ]

    for metric in metrics:
        # Metric value
        value_bbox = draw.textbbox((0, 0), metric["value"], font=metric_font)
        value_w = value_bbox[2] - value_bbox[0]
        draw.text(
            (metric["x"], metrics_y), metric["value"], fill="#107C10", font=metric_font
        )

        # Metric label
        label_bbox = draw.textbbox((0, 0), metric["label"], font=label_font)
        label_w = label_bbox[2] - label_bbox[0]
        draw.text(
            (metric["x"], metrics_y + 65),
            metric["label"],
            fill="#505050",
            font=label_font,
        )

    # Features section
    features_y = 420
    features = [
        "✓ Real-time EEG Processing",
        "✓ AI-Powered Personalization",
        "✓ Enterprise Security (HIPAA, GDPR, SOC 2)",
        "✓ Azure-Native Architecture",
        "✓ 99.9% Uptime SLA",
    ]

    for i, feature in enumerate(features):
        draw.text((180, features_y + i * 35), feature, fill="#505050", font=label_font)

    # Footer
    footer = "Azure Marketplace Ready | lifecoach-121.com"
    footer_bbox = draw.textbbox((0, 0), footer, font=label_font)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_w) // 2, 620), footer, fill="#0078D4", font=label_font)

    return img


def main():
    """Main execution function"""

    print("\n" + "=" * 60)
    print("L.I.F.E Platform - Azure Cloud Shell Screenshot Generator")
    print("=" * 60 + "\n")

    # Create output directory
    output_dir = "marketplace_assets"
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Output directory: {output_dir}/")

    # Generate screenshot
    try:
        img = create_marketplace_screenshot()

        # Save screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"LIFE_Platform_Screenshot_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)

        img.save(filepath, "PNG", quality=95, optimize=True)

        # Get file size
        file_size = os.path.getsize(filepath)
        file_size_kb = file_size / 1024

        print(f"\n✅ SUCCESS! Screenshot created:")
        print(f"   📁 File: {filepath}")
        print(f"   📏 Size: {img.width}x{img.height} pixels")
        print(f"   💾 Disk: {file_size_kb:.1f} KB")

        # Also create a standard named version
        standard_filename = "LIFE_Platform_Marketplace_Screenshot.png"
        standard_filepath = os.path.join(output_dir, standard_filename)
        img.save(standard_filepath, "PNG", quality=95, optimize=True)
        print(f"   📁 Also saved as: {standard_filepath}")

        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Download the screenshot from Cloud Shell:")
        print(f"   - Click 'Download' button in Cloud Shell toolbar")
        print(f"   - Enter path: {filepath}")
        print("   OR")
        print(f"   - Use: download {filepath}")
        print("")
        print("2. Upload to Partner Center:")
        print("   - Go to Offer Listing section")
        print("   - Scroll to 'Screenshots' area")
        print("   - Click 'Add screenshot'")
        print("   - Upload the downloaded PNG file")
        print("   - Add caption: 'L.I.F.E Platform - Key Performance Metrics'")
        print("=" * 60 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ ERROR: Failed to create screenshot")
        print(f"   {type(e).__name__}: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
