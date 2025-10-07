"""
L.I.F.E Platform - Visual Generator (Standalone)
No terminal required - Double-click to run!
"""

import os
import sys
import traceback


def main():
    """Generate visuals with error handling"""

    print("=" * 70)
    print("L.I.F.E PLATFORM - VISUAL GENERATOR")
    print("=" * 70)
    print()

    try:
        # Import PIL
        print("Checking Pillow installation...")
        from PIL import Image, ImageDraw, ImageFont

        print("✅ Pillow installed")
        print()
    except ImportError:
        print("❌ ERROR: Pillow not installed!")
        print()
        print("SOLUTION:")
        print("1. Open Command Prompt as Administrator")
        print("2. Run: pip install Pillow")
        print("3. Then run this script again")
        print()
        input("Press Enter to exit...")
        sys.exit(1)

    # Create output directory
    output_dir = "marketplace_assets"
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"✅ Created directory: {output_dir}/")
        print()
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    # Generate Logo
    print("-" * 70)
    print("GENERATING LOGO...")
    print("-" * 70)

    try:
        size = 280
        img = Image.new("RGB", (size, size), color="white")
        draw = ImageDraw.Draw(img)

        # Azure blue circle
        margin = 20
        draw.ellipse(
            [(margin, margin), (size - margin, size - margin)],
            fill="#0078D4",
            outline="#005A9E",
            width=4,
        )

        # Try to use Arial, fallback to default
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            subtitle_font = ImageFont.truetype("arial.ttf", 20)
        except Exception:
            print("Using default font (Arial not available)")
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

        # Save 280x280 logo
        logo_280_path = os.path.join(output_dir, "LIFE_Platform_Logo_280x280.png")
        img.save(logo_280_path, "PNG", quality=95, optimize=True)
        logo_280_size = os.path.getsize(logo_280_path) / 1024
        print(f"✅ Created: {logo_280_path}")
        print(f"   Size: {logo_280_size:.1f} KB")

        # Save 216x216 logo
        logo_216 = img.resize((216, 216), Image.Resampling.LANCZOS)
        logo_216_path = os.path.join(output_dir, "LIFE_Platform_Logo_216x216.png")
        logo_216.save(logo_216_path, "PNG", quality=95, optimize=True)
        logo_216_size = os.path.getsize(logo_216_path) / 1024
        print(f"✅ Created: {logo_216_path}")
        print(f"   Size: {logo_216_size:.1f} KB")
        print()

    except Exception as e:
        print(f"❌ Error generating logo: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

    # Generate Screenshot
    print("-" * 70)
    print("GENERATING SCREENSHOT...")
    print("-" * 70)

    try:
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), color="#F0F0F0")
        draw = ImageDraw.Draw(img)

        # Azure blue gradient background
        for y in range(height):
            color_value = int(0 + (240 - 0) * (y / height))
            draw.rectangle(
                [(0, y), (width, y + 1)], fill=(0, 120, 212 - color_value // 2)
            )

        # White content box
        box_margin = 80
        draw.rectangle(
            [(box_margin, box_margin), (width - box_margin, height - box_margin)],
            fill="white",
            outline="#0078D4",
            width=3,
        )

        # Try to use Arial
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            subtitle_font = ImageFont.truetype("arial.ttf", 24)
            text_font = ImageFont.truetype("arial.ttf", 20)
        except Exception:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Draw content
        y_pos = 120
        draw.text((150, y_pos), "L.I.F.E Platform", fill="#0078D4", font=title_font)
        y_pos += 70
        draw.text(
            (150, y_pos),
            "Neuroadaptive Learning System",
            fill="#333333",
            font=subtitle_font,
        )
        y_pos += 70

        metrics = [
            "✅ 95.8% Accuracy",
            "✅ 0.42ms Latency",
            "✅ 880x Faster than Competitors",
        ]

        for metric in metrics:
            draw.text((150, y_pos), metric, fill="#0078D4", font=text_font)
            y_pos += 45

        y_pos += 20
        draw.text((150, y_pos), "Features:", fill="#333333", font=text_font)
        y_pos += 40

        features = [
            "• Real-time EEG Processing",
            "• AI-Powered Personalization",
            "• Enterprise Security & Compliance",
            "• Azure-Native Integration",
            "• 99.9% Uptime SLA",
        ]

        for feature in features:
            draw.text((150, y_pos), feature, fill="#666666", font=text_font)
            y_pos += 35

        y_pos += 30
        draw.text(
            (150, y_pos), "Azure Marketplace Ready", fill="#0078D4", font=subtitle_font
        )
        y_pos += 40
        draw.text((150, y_pos), "lifecoach-121.com", fill="#666666", font=text_font)

        # Save screenshot
        screenshot_path = os.path.join(
            output_dir, "LIFE_Platform_Screenshot_1280x720.png"
        )
        img.save(screenshot_path, "PNG", quality=95, optimize=True)
        screenshot_size = os.path.getsize(screenshot_path) / 1024
        print(f"✅ Created: {screenshot_path}")
        print(f"   Size: {screenshot_size:.1f} KB")
        print()

    except Exception as e:
        print(f"❌ Error generating screenshot: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

    # Success summary
    print("=" * 70)
    print("✅ SUCCESS! ALL VISUALS GENERATED!")
    print("=" * 70)
    print()
    print(f"Files created in: {os.path.abspath(output_dir)}/")
    print()
    print("Files generated:")
    print("  1. LIFE_Platform_Logo_280x280.png")
    print("  2. LIFE_Platform_Logo_216x216.png")
    print("  3. LIFE_Platform_Screenshot_1280x720.png")
    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print()
    print("1. Open 'marketplace_assets' folder in File Explorer")
    print("2. Upload to Azure Marketplace Partner Center:")
    print("   - Offer Listing → Logo → Upload Logo_280x280.png")
    print("   - Offer Listing → Screenshots → Upload Screenshot_1280x720.png")
    print("3. Save draft in Partner Center")
    print()
    print("=" * 70)
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ UNEXPECTED ERROR")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        traceback.print_exc()
        print()
        input("Press Enter to exit...")
        input("Press Enter to exit...")
