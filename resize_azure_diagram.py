"""
Resize existing Azure architecture diagram for Partner Center
Converts 720x1280 to 1280x720 (landscape) for marketplace screenshot
"""

import os

from PIL import Image


def resize_architecture_diagram():
    """Resize the Azure cycle diagram to 1280x720 for Partner Center"""

    print("Resizing Azure architecture diagram...")

    # Input file (you'll need to save the attached image as this)
    input_file = "Azurecycle.png"
    output_file = "LIFE_Platform_Architecture_Screenshot_1280x720.png"

    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        print()
        print("Please save your attached image as 'Azurecycle.png' in this folder")
        print("Then run this script again.")
        return None

    try:
        # Open the image
        img = Image.open(input_file)
        print(f"✅ Loaded image: {img.size[0]}x{img.size[1]} pixels")

        # Target size for Partner Center
        target_width = 1280
        target_height = 720

        # Check if it's portrait (needs rotation) or landscape
        if img.size[1] > img.size[0]:
            print("📐 Image is portrait, rotating to landscape...")
            img = img.rotate(90, expand=True)

        # Calculate aspect ratio
        img_ratio = img.size[0] / img.size[1]
        target_ratio = target_width / target_height

        # Resize to fit within 1280x720 while maintaining aspect ratio
        if img_ratio > target_ratio:
            # Image is wider, fit to width
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            # Image is taller, fit to height
            new_height = target_height
            new_width = int(target_height * img_ratio)

        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"✅ Resized to: {new_width}x{new_height} pixels")

        # Create final canvas (1280x720) with white background
        final_img = Image.new("RGB", (target_width, target_height), "white")

        # Center the resized image on the canvas
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2

        final_img.paste(img_resized, (x_offset, y_offset))

        # Save
        final_img.save(output_file, "PNG", quality=95)
        print(f"✅ Saved as: {output_file}")
        print(f"✅ Final size: {target_width}x{target_height} pixels")
        print()
        print("🎯 Perfect for Partner Center upload!")

        return output_file

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    print("=" * 70)
    print("L.I.F.E Platform Architecture Diagram Resizer")
    print("Converting to 1280x720 for Azure Marketplace")
    print("=" * 70)
    print()

    result = resize_architecture_diagram()

    if result:
        print()
        print("=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Upload to Partner Center > Offer Listing > Screenshots")
        print("2. Add caption: 'L.I.F.E Platform Architecture - Azure-Native Design'")
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("⚠️ Action needed:")
        print("1. Save your attached diagram as 'Azurecycle.png'")
        print("2. Run this script again")
        print("=" * 70)
        print("2. Run this script again")
        print("=" * 70)
