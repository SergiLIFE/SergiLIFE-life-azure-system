"""Simple visual generator - guaranteed to work!"""

import os

from PIL import Image, ImageDraw, ImageFont

# Create output directory
os.makedirs("marketplace_assets", exist_ok=True)

print("Creating visuals...")

# Create 280x280 logo
img = Image.new("RGB", (280, 280), color="white")
draw = ImageDraw.Draw(img)
draw.ellipse([20, 20, 260, 260], fill="#0078D4")
try:
    font = ImageFont.truetype("arial.ttf", 32)
except:
    font = ImageFont.load_default()
draw.text((140, 140), "L.I.F.E", fill="white", anchor="mm", font=font)
img.save("marketplace_assets/LIFE_Platform_Logo_280x280.png")
print("✅ Created 280x280 logo")

# Create 216x216 logo
img_small = img.resize((216, 216), Image.LANCZOS)
img_small.save("marketplace_assets/LIFE_Platform_Logo_216x216.png")
print("✅ Created 216x216 logo")

# Create 1280x720 screenshot
screenshot = Image.new("RGB", (1280, 720), color="#E8F4FF")
draw = ImageDraw.Draw(screenshot)
# Header
draw.rectangle([0, 0, 1280, 100], fill="#0078D4")
draw.text((640, 50), "L.I.F.E Platform Dashboard", fill="white", anchor="mm", font=font)
# Metrics
draw.rectangle([50, 150, 400, 350], fill="white", outline="#0078D4", width=3)
draw.text((225, 200), "95.8% Accuracy", fill="#0078D4", anchor="mm", font=font)
draw.rectangle([450, 150, 800, 350], fill="white", outline="#0078D4", width=3)
draw.text((625, 200), "0.42ms Latency", fill="#0078D4", anchor="mm", font=font)
draw.rectangle([850, 150, 1200, 350], fill="white", outline="#0078D4", width=3)
draw.text((1025, 200), "880x Faster", fill="#0078D4", anchor="mm", font=font)
screenshot.save("marketplace_assets/LIFE_Platform_Screenshot_1280x720.png")
print("✅ Created 1280x720 screenshot")

print("\n🎉 SUCCESS! All files created in marketplace_assets/")
print("Files created:")
print("  - LIFE_Platform_Logo_280x280.png")
print("  - LIFE_Platform_Logo_216x216.png")
print("  - LIFE_Platform_Screenshot_1280x720.png")
print("  - LIFE_Platform_Screenshot_1280x720.png")
