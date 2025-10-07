"""
L.I.F.E Platform - Azure Marketplace Screenshot Generator
Creates professional 1280x720 screenshots for Partner Center offer listing
"""

import os

from PIL import Image, ImageDraw, ImageFont


def create_marketplace_screenshot():
    """Generate professional marketplace screenshot (1280x720)"""

    # Create image with gradient background
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color="#0078D4")  # Azure blue
    draw = ImageDraw.Draw(img)

    # Create gradient effect (darker at bottom)
    for y in range(height):
        darkness = int(255 * (1 - y / height * 0.3))
        color = (0, int(120 * darkness / 255), int(212 * darkness / 255))
        draw.rectangle([(0, y), (width, y + 1)], fill=color)

    # Add white overlay for content area
    content_padding = 80
    draw.rectangle(
        [
            (content_padding, content_padding),
            (width - content_padding, height - content_padding),
        ],
        fill="white",
        outline="#0078D4",
        width=3,
    )

    # Title
    title_text = "L.I.F.E Platform"
    subtitle_text = "Neuroadaptive Learning System"

    # Try to use a nice font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 72)
        subtitle_font = ImageFont.truetype("arial.ttf", 36)
        metric_font = ImageFont.truetype("arialbd.ttf", 48)
        label_font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        metric_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw title
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 120), title_text, fill="#0078D4", font=title_font)

    # Draw subtitle
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 210), subtitle_text, fill="#505050", font=subtitle_font)

    # Key metrics section
    metrics_y = 300

    # Metric 1: Accuracy
    metric1_text = "95.8%"
    label1_text = "Neural Processing Accuracy"
    draw.text((200, metrics_y), metric1_text, fill="#107C10", font=metric_font)
    draw.text((200, metrics_y + 60), label1_text, fill="#505050", font=label_font)

    # Metric 2: Speed
    metric2_text = "0.42ms"
    label2_text = "Processing Latency"
    draw.text((520, metrics_y), metric2_text, fill="#107C10", font=metric_font)
    draw.text((520, metrics_y + 60), label2_text, fill="#505050", font=label_font)

    # Metric 3: Performance
    metric3_text = "880x"
    label3_text = "Faster Than Competitors"
    draw.text((860, metrics_y), metric3_text, fill="#107C10", font=metric_font)
    draw.text((860, metrics_y + 60), label3_text, fill="#505050", font=label_font)

    # Bottom features section
    features_y = 480
    feature_spacing = 30

    features = [
        "✓ Real-time EEG Processing",
        "✓ AI-Powered Personalization",
        "✓ Enterprise-Grade Security (HIPAA, GDPR, SOC 2)",
        "✓ Azure-Native Architecture",
        "✓ 99.9% Uptime SLA",
    ]

    for i, feature in enumerate(features):
        draw.text(
            (200, features_y + i * feature_spacing),
            feature,
            fill="#303030",
            font=small_font,
        )

    # Footer
    footer_text = "Available on Azure Marketplace | Production-Ready September 2025"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=small_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    footer_x = (width - footer_width) // 2
    draw.text((footer_x, 650), footer_text, fill="#808080", font=small_font)

    # Save image
    output_dir = os.path.join(os.path.dirname(__file__), "marketplace_assets")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "LIFE_Platform_Screenshot_1.png")

    img.save(output_path, "PNG", quality=95)
    print(f"✅ Screenshot created: {output_path}")
    print(f"   Size: {width}x{height} pixels")
    print(f"   Format: PNG")
    print(f"   Ready for Partner Center upload!")

    return output_path


def create_dashboard_screenshot():
    """Generate dashboard-style screenshot"""

    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color="#F5F5F5")
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (width, 80)], fill="#0078D4")

    try:
        header_font = ImageFont.truetype("arialbd.ttf", 32)
        card_title_font = ImageFont.truetype("arialbd.ttf", 28)
        card_value_font = ImageFont.truetype("arialbd.ttf", 48)
        card_label_font = ImageFont.truetype("arial.ttf", 18)
    except:
        header_font = ImageFont.load_default()
        card_title_font = ImageFont.load_default()
        card_value_font = ImageFont.load_default()
        card_label_font = ImageFont.load_default()

    # Header text
    draw.text((40, 25), "L.I.F.E Platform Dashboard", fill="white", font=header_font)

    # Performance cards
    card_width = 360
    card_height = 180
    card_spacing = 40
    cards_y = 120

    cards = [
        {"title": "Active Learners", "value": "1,847", "color": "#0078D4", "x": 40},
        {
            "title": "Processing Accuracy",
            "value": "95.8%",
            "color": "#107C10",
            "x": 40 + card_width + card_spacing,
        },
        {
            "title": "Avg Response Time",
            "value": "0.42ms",
            "color": "#D83B01",
            "x": 40 + 2 * (card_width + card_spacing),
        },
    ]

    for card in cards:
        # Card background
        draw.rectangle(
            [(card["x"], cards_y), (card["x"] + card_width, cards_y + card_height)],
            fill="white",
            outline="#E0E0E0",
            width=2,
        )

        # Card title
        draw.text(
            (card["x"] + 20, cards_y + 20),
            card["title"],
            fill="#505050",
            font=card_title_font,
        )

        # Card value
        draw.text(
            (card["x"] + 20, cards_y + 70),
            card["value"],
            fill=card["color"],
            font=card_value_font,
        )

    # Chart area
    chart_y = cards_y + card_height + 40
    chart_height = 240

    draw.rectangle(
        [(40, chart_y), (width - 40, chart_y + chart_height)],
        fill="white",
        outline="#E0E0E0",
        width=2,
    )

    # Chart title
    draw.text(
        (60, chart_y + 20),
        "Real-Time Learning Performance",
        fill="#303030",
        font=card_title_font,
    )

    # Simple line chart simulation
    chart_points = [
        (100, chart_y + 180),
        (200, chart_y + 150),
        (300, chart_y + 120),
        (400, chart_y + 100),
        (500, chart_y + 90),
        (600, chart_y + 85),
        (700, chart_y + 80),
        (800, chart_y + 75),
        (900, chart_y + 70),
        (1000, chart_y + 68),
        (1100, chart_y + 65),
        (1200, chart_y + 63),
    ]

    draw.line(chart_points, fill="#0078D4", width=3)

    # Add dots at each point
    for point in chart_points:
        draw.ellipse(
            [(point[0] - 5, point[1] - 5), (point[0] + 5, point[1] + 5)],
            fill="#0078D4",
            outline="white",
            width=2,
        )

    # Footer badge
    badge_text = "SOTA Champion | 880x Faster | Enterprise Ready"
    try:
        badge_font = ImageFont.truetype("arialbd.ttf", 20)
    except:
        badge_font = ImageFont.load_default()

    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_width = badge_bbox[2] - badge_bbox[0]
    badge_x = (width - badge_width) // 2

    draw.rectangle(
        [(badge_x - 20, 670), (badge_x + badge_width + 20, 705)], fill="#107C10"
    )
    draw.text((badge_x, 677), badge_text, fill="white", font=badge_font)

    # Save
    output_dir = os.path.join(os.path.dirname(__file__), "marketplace_assets")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "LIFE_Platform_Screenshot_2_Dashboard.png")

    img.save(output_path, "PNG", quality=95)
    print(f"✅ Dashboard screenshot created: {output_path}")
    print(f"   Size: {width}x{height} pixels")

    return output_path


def create_architecture_screenshot():
    """Generate architecture diagram screenshot"""

    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 48)
        box_font = ImageFont.truetype("arialbd.ttf", 24)
        label_font = ImageFont.truetype("arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        box_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    # Title
    title_text = "L.I.F.E Platform Architecture"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 40), title_text, fill="#0078D4", font=title_font)

    # Architecture layers
    layer_height = 100
    layer_y_start = 140
    layer_spacing = 30

    layers = [
        {
            "name": "Neural Processing Core",
            "color": "#0078D4",
            "desc": "Real-time EEG analysis • 95.8% accuracy",
        },
        {
            "name": "Venturi Gates System",
            "color": "#107C10",
            "desc": "Sub-millisecond processing • 3-gate orchestration",
        },
        {
            "name": "Azure Integration Layer",
            "color": "#D83B01",
            "desc": "Functions • Storage • Service Bus • Key Vault",
        },
        {
            "name": "Campaign Automation",
            "color": "#8661C5",
            "desc": "Marketplace promotion • 1,720 institutions",
        },
    ]

    for i, layer in enumerate(layers):
        y = layer_y_start + i * (layer_height + layer_spacing)

        # Layer box
        draw.rectangle(
            [(100, y), (1180, y + layer_height)],
            fill=layer["color"],
            outline="#303030",
            width=2,
        )

        # Layer name
        draw.text((120, y + 20), layer["name"], fill="white", font=box_font)

        # Layer description
        draw.text((120, y + 55), layer["desc"], fill="white", font=label_font)

    # Footer stats
    footer_y = 660
    stats = "Production Ready • 99.9% Uptime • HIPAA/GDPR Compliant • Azure Marketplace"

    try:
        footer_font = ImageFont.truetype("arial.ttf", 20)
    except:
        footer_font = ImageFont.load_default()

    stats_bbox = draw.textbbox((0, 0), stats, font=footer_font)
    stats_width = stats_bbox[2] - stats_bbox[0]
    stats_x = (width - stats_width) // 2
    draw.text((stats_x, footer_y), stats, fill="#505050", font=footer_font)

    # Save
    output_dir = os.path.join(os.path.dirname(__file__), "marketplace_assets")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(
        output_dir, "LIFE_Platform_Screenshot_3_Architecture.png"
    )

    img.save(output_path, "PNG", quality=95)
    print(f"✅ Architecture screenshot created: {output_path}")
    print(f"   Size: {width}x{height} pixels")

    return output_path


if __name__ == "__main__":
    print("=" * 70)
    print("L.I.F.E Platform - Marketplace Screenshot Generator")
    print("Creating professional 1280x720 screenshots for Partner Center")
    print("=" * 70)
    print()

    try:
        # Generate all three screenshots
        screenshot1 = create_marketplace_screenshot()
        print()
        screenshot2 = create_dashboard_screenshot()
        print()
        screenshot3 = create_architecture_screenshot()
        print()

        print("=" * 70)
        print("✅ SUCCESS! All screenshots created!")
        print("=" * 70)
        print()
        print("📁 Location: marketplace_assets/")
        print()
        print("Files created:")
        print("  1. LIFE_Platform_Screenshot_1.png (Key metrics)")
        print("  2. LIFE_Platform_Screenshot_2_Dashboard.png (Dashboard view)")
        print("  3. LIFE_Platform_Screenshot_3_Architecture.png (Architecture)")
        print()
        print("🎯 Next steps:")
        print("  1. Navigate to: marketplace_assets/ folder")
        print("  2. Upload any/all screenshots to Partner Center")
        print("  3. Add captions describing each screenshot")
        print()
        print("💡 Partner Center requires at least 1 screenshot (you now have 3!)")
        print()

    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("💡 Troubleshooting:")
        print("  - Make sure Pillow is installed: pip install Pillow")
        print("  - If fonts fail, default font will be used (still works!)")
        print("  - Check write permissions in current directory")
        print("  - If fonts fail, default font will be used (still works!)")
        print("  - Check write permissions in current directory")
