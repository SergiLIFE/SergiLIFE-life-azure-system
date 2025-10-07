# Screenshot Resize Guide for Azure Marketplace
**L.I.F.E. Platform - Final Launch Day - September 27, 2025**

## Current Screenshots Created ✅
- `neuroadaptive.png` - L.I.F.E. Theory logo/branding
- `azurediagram.png` - Azure architecture diagram

## Marketplace Requirements
- **Required Size:** 1280x720 pixels (16:9 aspect ratio)
- **Format:** PNG or JPG
- **Maximum:** 5 screenshots
- **Recommended:** 3-5 high-quality screenshots

## Quick Resize Options

### Option 1: Windows Paint (Fastest - 2 minutes)
1. **Open Paint** → File → Open → Select your screenshot
2. **Resize** → Home tab → Resize button
3. **Set to:** 1280 x 720 pixels (uncheck "Maintain aspect ratio" if needed)
4. **Save As** → PNG format
5. **Repeat** for both screenshots

### Option 2: Online Tool (3 minutes)
1. Go to **resize-image.net** or **canva.com**
2. Upload your images
3. Set dimensions to **1280x720**
4. Download resized versions

### Option 3: PowerShell Resize (If you have ImageMagick)
```powershell
# Install ImageMagick first: winget install ImageMagick.ImageMagick
magick "c:\Users\Sergio Paya Borrull\OneDrive\Pictures\neuroadaptive.png" -resize 1280x720! "neuroadaptive_marketplace.png"
magick "c:\Users\Sergio Paya Borrull\OneDrive\Pictures\azurediagram.png" -resize 1280x720! "azurediagram_marketplace.png"
```

## Recommended Marketplace Sequence
1. **Screenshot 1:** Azure Architecture Diagram (shows technical credibility)
2. **Screenshot 2:** L.I.F.E. Theory Branding (shows professional identity)
3. **Screenshot 3:** (Optional) Live Azure Container Apps dashboard
4. **Screenshot 4:** (Optional) EEG data processing interface
5. **Screenshot 5:** (Optional) Analytics dashboard

## Next Steps After Resize
1. ✅ Copy resized images to workspace folder
2. ✅ Upload to Partner Center marketplace form
3. ✅ Complete final 2 remaining fields (logos, privacy policy)
4. ✅ Submit offer for Microsoft certification
5. ✅ Call +1-800-PARTNER for expedited review

## File Naming Convention
- `life_platform_architecture_1280x720.png`
- `life_platform_branding_1280x720.png`
- `life_platform_dashboard_1280x720.png`

## Quality Check
- ✅ **Clarity:** Text should be readable at marketplace preview size
- ✅ **Professional:** Clean, branded appearance
- ✅ **Relevant:** Shows actual platform capabilities
- ✅ **Optimized:** File size under 2MB each

---
**Time Estimate:** 5-10 minutes to resize and upload
**Impact:** Completes 80% of remaining marketplace requirements
**Launch Status:** Ready for same-day submission on September 27, 2025! 🚀