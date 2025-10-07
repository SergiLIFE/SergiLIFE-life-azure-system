"""Ultra-simple visual generator with full error reporting"""

import os
import sys

print("=" * 70)
print("STEP 1: Checking Python and Pillow")
print("=" * 70)
print(f"Python: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    from PIL import Image, ImageDraw, ImageFont

    print("✅ Pillow is installed and working!")
except ImportError as e:
    print(f"❌ ERROR: Cannot import Pillow: {e}")
    print("Run: pip install Pillow")
    sys.exit(1)

print("\n" + "=" * 70)
print("STEP 2: Creating marketplace_assets folder")
print("=" * 70)
try:
    os.makedirs("marketplace_assets", exist_ok=True)
    print(f"✅ Folder created at: {os.path.abspath('marketplace_assets')}")
except Exception as e:
    print(f"❌ ERROR creating folder: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("STEP 3: Creating Logo (280x280)")
print("=" * 70)
try:
    img = Image.new("RGB", (280, 280), color="white")
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 260, 260], fill="#0078D4")
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
    draw.text((140, 140), "L.I.F.E", fill="white", anchor="mm", font=font)
    img.save("marketplace_assets/LIFE_Platform_Logo_280x280.png")
    print("✅ Logo 280x280 created successfully!")
except Exception as e:
    print(f"❌ ERROR creating logo: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("STEP 4: Creating Logo (216x216)")
print("=" * 70)
try:
    img_small = img.resize((216, 216), Image.LANCZOS)
    img_small.save("marketplace_assets/LIFE_Platform_Logo_216x216.png")
    print("✅ Logo 216x216 created successfully!")
except Exception as e:
    print(f"❌ ERROR creating small logo: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("STEP 5: Creating Screenshot (1280x720)")
print("=" * 70)
try:
    screenshot = Image.new("RGB", (1280, 720), color="#E8F4FF")
    draw = ImageDraw.Draw(screenshot)
    draw.rectangle([0, 0, 1280, 100], fill="#0078D4")
    draw.text(
        (640, 50), "L.I.F.E Platform Dashboard", fill="white", anchor="mm", font=font
    )
    draw.rectangle([50, 150, 400, 350], fill="white", outline="#0078D4", width=3)
    draw.text((225, 200), "95.8% Accuracy", fill="#0078D4", anchor="mm", font=font)
    draw.rectangle([450, 150, 800, 350], fill="white", outline="#0078D4", width=3)
    draw.text((625, 200), "0.42ms Latency", fill="#0078D4", anchor="mm", font=font)
    draw.rectangle([850, 150, 1200, 350], fill="white", outline="#0078D4", width=3)
    draw.text((1025, 200), "880x Faster", fill="#0078D4", anchor="mm", font=font)
    screenshot.save("marketplace_assets/LIFE_Platform_Screenshot_1280x720.png")
    print("✅ Screenshot 1280x720 created successfully!")
except Exception as e:
    print(f"❌ ERROR creating screenshot: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("SUCCESS! ALL FILES CREATED!")
print("=" * 70)
print(f"\nFiles created in: {os.path.abspath('marketplace_assets')}")
print("\nFiles:")
print("  1. LIFE_Platform_Logo_280x280.png")
print("  2. LIFE_Platform_Logo_216x216.png")
print("  3. LIFE_Platform_Screenshot_1280x720.png")
print("\nYou can now upload these to Partner Center!")
print("=" * 70)
