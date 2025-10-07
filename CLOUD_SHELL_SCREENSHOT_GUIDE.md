# Azure Cloud Shell Screenshot Generation Guide

## Quick Start (3 Commands)

You're currently in **Azure Cloud Shell**, which runs Linux. Here's how to generate your marketplace screenshot:

```bash
# Step 1: Setup environment (installs Pillow)
bash cloudshell_setup.sh

# Step 2: Generate screenshot
python3 cloudshell_screenshot_generator.py

# Step 3: Download the file
download marketplace_assets/LIFE_Platform_Marketplace_Screenshot.png
```

---

## Detailed Instructions

### Current Situation
You ran commands in Azure Cloud Shell (PowerShell on Linux):
```powershell
PS /home/sergio> cd "c:\Users\Sergio Paya Borrull\..."
# ❌ This fails because Windows paths don't exist in Cloud Shell
```

**Solution:** Use the Cloud Shell-compatible scripts created above.

---

## Method 1: Cloud Shell Screenshot Generation (RECOMMENDED)

### Step 1: Install Dependencies

```bash
bash cloudshell_setup.sh
```

**What this does:**
- Checks Python3 installation
- Installs Pillow library in user space
- Creates output directories
- Verifies installation

**Expected output:**
```
==================================================
L.I.F.E Platform - Azure Cloud Shell Setup
==================================================

Checking Python installation...
Python 3.9.x

Installing Pillow library...
Collecting Pillow...
Successfully installed Pillow-x.x.x

✅ Pillow installed successfully!
```

### Step 2: Generate Screenshot

```bash
python3 cloudshell_screenshot_generator.py
```

**Expected output:**
```
============================================================
L.I.F.E Platform - Azure Cloud Shell Screenshot Generator
============================================================

✅ Output directory: marketplace_assets/
Creating L.I.F.E Platform marketplace screenshot...

✅ SUCCESS! Screenshot created:
   📁 File: marketplace_assets/LIFE_Platform_Screenshot_20250930_143022.png
   📏 Size: 1280x720 pixels
   💾 Disk: 156.2 KB
   📁 Also saved as: marketplace_assets/LIFE_Platform_Marketplace_Screenshot.png
```

### Step 3: Download from Cloud Shell

**Option A: Cloud Shell Download Command**
```bash
download marketplace_assets/LIFE_Platform_Marketplace_Screenshot.png
```

**Option B: Cloud Shell UI Download**
1. Click the **Upload/Download** button (📤) in Cloud Shell toolbar
2. Click **Download**
3. Enter path: `marketplace_assets/LIFE_Platform_Marketplace_Screenshot.png`
4. File downloads to your local computer

### Step 4: Upload to Partner Center

1. Go to [Partner Center](https://partner.microsoft.com/dashboard/marketplace-offers/overview)
2. Navigate to your offer: **L.I.F.E_Theory_SaaS**
3. Click **Offer listing** section
4. Scroll to **Screenshots** area
5. Click **Add screenshot**
6. Upload the downloaded PNG file (1280x720, ~150KB)
7. Add caption: `L.I.F.E Platform - Neural Processing Performance Metrics`
8. Click **Save draft**

---

## Method 2: Local Windows Generation (Alternative)

If you want to run locally on Windows instead of Cloud Shell:

### Prerequisites
```cmd
cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
.venv\Scripts\activate
pip install Pillow
```

### Run Script
```cmd
python create_screenshot_simple.py
```

### Output Location
```
marketplace_assets\LIFE_Platform_Screenshot_20250930_143022.png
```

---

## Troubleshooting

### Issue: "bash: cloudshell_setup.sh: Permission denied"
**Solution:**
```bash
chmod +x cloudshell_setup.sh
bash cloudshell_setup.sh
```

### Issue: "ModuleNotFoundError: No module named 'PIL'"
**Solution:**
```bash
pip install --user Pillow
# Then retry: python3 cloudshell_screenshot_generator.py
```

### Issue: "No such file or directory"
**Solution:** Make sure you're in the repository directory:
```bash
cd ~/SergiLIFE-life-azure-system  # Or wherever you cloned the repo
ls -la cloudshell_screenshot_generator.py  # Verify file exists
```

### Issue: Windows paths in Cloud Shell
**Problem:**
```powershell
cd "c:\Users\Sergio Paya Borrull\..."
# Set-Location: Cannot find drive. A drive with the name 'c' does not exist.
```

**Explanation:** Azure Cloud Shell runs Linux, not Windows. Windows paths (c:\...) don't exist.

**Solution:** Use Linux paths:
```bash
cd ~  # Your home directory
cd ~/SergiLIFE-life-azure-system  # If repo is cloned here
pwd  # Check current directory
```

---

## Screenshot Specifications

✅ **Partner Center Requirements Met:**
- Dimensions: 1280x720 pixels (exact)
- Format: PNG (high quality)
- File size: ~150KB (under 2MB limit)
- Content: Professional branding with key metrics

✅ **Content Included:**
- L.I.F.E Platform branding
- "Neuroadaptive Learning System" tagline
- 3 key performance metrics:
  - 95.8% Neural Processing Accuracy
  - 0.42ms Processing Latency
  - 880x Faster Than Competitors
- 5 feature highlights
- Azure Marketplace Ready badge
- Domain: lifecoach-121.com

---

## What's Next After Screenshot?

### Immediate Tasks
1. ✅ Generate screenshot (use Cloud Shell script above)
2. ✅ Download screenshot to local computer
3. ✅ Upload to Partner Center Offer Listing
4. ⏳ Create logo (216x216 PNG) - **CRITICAL BLOCKER**
5. ⏳ Upload logo to Partner Center
6. ⏳ Complete all Offer Listing fields
7. ⏳ Save Offer Listing draft

### Then Create Pricing Plans (CRITICAL BLOCKER)
- Basic Plan: $15/user/month
- Professional Plan: $30/user/month
- Enterprise Plan: $50/user/month

### Finally Submit for Certification
- Complete all sections
- Click "Review and publish"
- Microsoft certification: 1-3 business days
- **Deadline:** Must be approved by October 7, 2025

---

## File Locations

### Cloud Shell (Linux paths)
```
~/SergiLIFE-life-azure-system/
├── cloudshell_setup.sh                    # Setup script
├── cloudshell_screenshot_generator.py     # Screenshot generator
├── marketplace_assets/                    # Output directory
│   ├── LIFE_Platform_Screenshot_*.png    # Timestamped version
│   └── LIFE_Platform_Marketplace_Screenshot.png  # Standard name
└── logs/                                  # Logs directory
```

### Local Windows (if running locally)
```
c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system\
├── create_screenshot_simple.py
├── marketplace_assets\
│   └── LIFE_Platform_Screenshot_*.png
```

---

## Current Cloud Shell Context

You're authenticated to Azure Cloud Shell at:
- Path: `/home/sergio`
- Shell: PowerShell on Linux
- Python: Available as `python3`
- Storage: Persistent across sessions

**Repository location:** You need to navigate to your repository directory. Try:
```bash
cd ~
ls -la
# Look for SergiLIFE-life-azure-system directory
cd SergiLIFE-life-azure-system  # Or wherever it is
```

---

## Summary

✅ **Use Cloud Shell scripts** (cloudshell_*.py and cloudshell_*.sh)  
❌ **Don't use Windows scripts** in Cloud Shell (.bat files, Windows paths)

**3-command workflow:**
1. `bash cloudshell_setup.sh` - One-time setup
2. `python3 cloudshell_screenshot_generator.py` - Generate screenshot
3. `download marketplace_assets/LIFE_Platform_Marketplace_Screenshot.png` - Download to local

Then upload to Partner Center Offer Listing section.

**Timeline:** 7 days until October 7 launch - generate screenshot TODAY!
