"""
Simple Screenshot Generator - 1280x720 for Azure Marketplace
Creates basic but professional screenshots using Pillow
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont


def create_simple_screenshot():
    """Create a simple but professional 1280x720 screenshot"""

    print("Creating screenshot...")

    # Image size
    width, height = 1280, 720

    # Create image with Azure blue background
    img = Image.new("RGB", (width, height), color="#0078D4")
    draw = ImageDraw.Draw(img)

    # Create white content area
    margin = 60
    draw.rectangle(
        [(margin, margin), (width - margin, height - margin)],
        fill="white",
        outline="#0078D4",
        width=4,
    )

    # Use default font (always works)
    from PIL import ImageFont

    try:
        # Try to use Arial if available
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 30)
        metric_font = ImageFont.truetype("arialbd.ttf", 40)
        text_font = ImageFont.truetype("arial.ttf", 22)
    except:
        # Fallback to default
        print("Using default font...")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        metric_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Title
    title = "L.I.F.E Platform"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 100), title, fill="#0078D4", font=title_font)

    # Subtitle
    subtitle = "Neuroadaptive Learning System"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(
        ((width - subtitle_w) // 2, 180), subtitle, fill="#666666", font=subtitle_font
    )

    # Key metrics boxes
    box_y = 260
    box_width = 330
    box_height = 160
    spacing = 50

    metrics = [
        {"value": "95.8%", "label": "Neural Processing\nAccuracy", "x": 100},
        {
            "value": "0.42ms",
            "label": "Processing\nLatency",
            "x": 100 + box_width + spacing,
        },
        {
            "value": "880x",
            "label": "Faster Than\nCompetitors",
            "x": 100 + 2 * (box_width + spacing),
        },
    ]

    for metric in metrics:
        # Box background
        draw.rectangle(
            [(metric["x"], box_y), (metric["x"] + box_width, box_y + box_height)],
            fill="#F0F0F0",
            outline="#0078D4",
            width=2,
        )

        # Value
        val_bbox = draw.textbbox((0, 0), metric["value"], font=metric_font)
        val_w = val_bbox[2] - val_bbox[0]
        draw.text(
            (metric["x"] + (box_width - val_w) // 2, box_y + 30),
            metric["value"],
            fill="#107C10",
            font=metric_font,
        )

        # Label
        lines = metric["label"].split("\n")
        y_offset = box_y + 90
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=text_font)
            line_w = line_bbox[2] - line_bbox[0]
            draw.text(
                (metric["x"] + (box_width - line_w) // 2, y_offset),
                line,
                fill="#333333",
                font=text_font,
            )
            y_offset += 28

    # Features list
    features_y = 460
    features = [
        "Real-time EEG Processing",
        "AI-Powered Personalization",
        "Enterprise-Grade Security",
        "Azure-Native Architecture",
    ]

    for i, feature in enumerate(features):
        draw.text(
            (120, features_y + i * 35), f"✓ {feature}", fill="#333333", font=text_font
        )

    # Footer
    footer = "Available on Azure Marketplace | Production-Ready"
    footer_bbox = draw.textbbox((0, 0), footer, font=text_font)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_w) // 2, 640), footer, fill="#666666", font=text_font)

    # Save
    output_dir = os.path.dirname(__file__)
    if not output_dir:
        output_dir = "."

    output_path = os.path.join(output_dir, "LIFE_Platform_Screenshot_1280x720.png")
    img.save(output_path, "PNG")

    print(f"\n✅ SUCCESS!")
    print(f"Screenshot saved to: {output_path}")
    print(f"Size: {width}x{height} pixels")
    print(f"Format: PNG")
    print(f"\n🎯 Ready to upload to Partner Center!")

    return output_path


if __name__ == "__main__":
    try:
        print("=" * 70)
        print("L.I.F.E Platform Screenshot Generator")
        print("Creating 1280x720 screenshot for Azure Marketplace")
        print("=" * 70)
        print()

        create_simple_screenshot()

        print()
        print("=" * 70)
        print("Next steps:")
        print("1. Find the file: LIFE_Platform_Screenshot_1280x720.png")
        print("2. Upload to Partner Center > Offer Listing > Screenshots")
        print("3. Add caption: 'L.I.F.E Platform Key Performance Metrics'")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
        traceback.print_exc()
        sys.exit(1)
