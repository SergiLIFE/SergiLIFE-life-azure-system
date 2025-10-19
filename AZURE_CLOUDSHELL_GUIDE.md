# 🌐 L.I.F.E. Research Platform - Azure Cloud Shell Deployment Guide

**Copyright 2025 - Sergio Paya Borrull**  
**Quick Guide to Deploy and Use Research Library in Azure Cloud Shell**

---

## 🚀 Step-by-Step Deployment

### **Step 1: Upload Files to Cloud Shell**

You have **two options** to get the research library into Azure Cloud Shell:

#### **Option A: Upload from Local Machine (Recommended)**

1. In Azure Cloud Shell, click the **Upload/Download files** icon (↑↓)
2. Select **Upload**
3. Upload these 3 files:
   - `research_data_library.py`
   - `populate_research_database.py`
   - `validate_research_integration.py`

#### **Option B: Clone from GitHub (If pushed to repo)**

```bash
cd ~
git clone https://github.com/SergiLIFE/SergiLIFE-life-azure-system.git
cd SergiLIFE-life-azure-system
```

---

### **Step 2: Set Up Project Directory**

```bash
# Create project directory
mkdir -p ~/life-research-platform
cd ~/life-research-platform

# If you uploaded files, move them here
mv ~/research_data_library.py .
mv ~/populate_research_database.py .
mv ~/validate_research_integration.py .

# Or if cloned from GitHub, copy them
# cp ~/SergiLIFE-life-azure-system/*.py .
```

---

### **Step 3: Verify Python is Available**

```bash
# Check Python version
python3 --version

# Should show Python 3.8 or higher
```

---

### **Step 4: Run Quick Test**

Create a quick test script:

```bash
cat > test_library.py << 'EOF'
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from research_data_library import initialize_research_library
import random

print("="*70)
print("L.I.F.E. RESEARCH LIBRARY - QUICK TEST")
print("="*70)

library = initialize_research_library()
print(f"✓ Library v{library.version} initialized")

# Test EEG processing
raw_eeg = [random.uniform(10, 30) for _ in range(256)]
result = library.process_raw_eeg(raw_eeg, sampling_rate=256)
print(f"✓ EEG Processing: Engagement={result['engagement']:.3f}")

# Test statistical analysis
control = [65, 68, 72, 70, 71]
intervention = [78, 82, 79, 85, 81]
t_result = library.calculate_t_test(control, intervention)
print(f"✓ Statistics: p={t_result.p_value:.4f}, d={t_result.effect_size:.3f}")

print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
EOF

# Run the test
python3 test_library.py
```

---

## 💻 Using the Library in Cloud Shell

### **Interactive Python Mode**

```bash
python3
```

Then in Python:

```python
from research_data_library import initialize_research_library
import random

# Initialize library
library = initialize_research_library()

# Process EEG data
raw_eeg = [random.uniform(10, 30) for _ in range(256)]
result = library.process_raw_eeg(raw_eeg, sampling_rate=256)

print(f"Engagement: {result['engagement']:.3f}")
print(f"Focus: {result['focus']:.3f}")
print(f"Quality: {result['quality_score']:.3f}")

# Run statistical analysis
control = [65.2, 68.4, 72.1, 69.8, 71.3]
intervention = [78.5, 82.1, 79.3, 85.2, 80.9]
t_result = library.calculate_t_test(control, intervention)

print(t_result.interpretation)

# Exit Python
exit()
```

---

### **Populate Full Research Database**

```bash
python3 populate_research_database.py
```

**Expected Output:**
```
✓ Created Educational Neuroscience Study: 120 participants, 1440 sessions
✓ Created Clinical ADHD Study: 60 participants, 1200 sessions
✓ Created University Cognitive Study: 150 participants, 2250 sessions
✓ Created Longitudinal Study: 80 participants, 1920 sessions
✓ Created Enterprise Training Study: 200 participants, 2000 sessions

Total Studies: 5
Total Participants: 610
Total Sessions: 8810
```

---

### **Run Comprehensive Validation**

```bash
python3 validate_research_integration.py
```

---

## 📝 Sample Analysis Script

Create a custom analysis script:

```bash
cat > my_analysis.py << 'EOF'
from research_data_library import initialize_research_library
import random

# Initialize
library = initialize_research_library()

# Create sample data
print("Generating sample EEG data...")
for i in range(5):
    raw_eeg = [random.uniform(10, 30) for _ in range(256)]
    result = library.process_raw_eeg(raw_eeg, sampling_rate=256)
    
    print(f"\nSample {i+1}:")
    print(f"  Engagement: {result['engagement']:.3f}")
    print(f"  Focus: {result['focus']:.3f}")
    print(f"  Stress: {result['stress']:.3f}")

# Compare groups
control = [65, 68, 72, 70, 71, 69, 73, 67, 71, 70]
intervention = [78, 82, 79, 85, 81, 83, 80, 84, 82, 79]

t_result = library.calculate_t_test(control, intervention)

print("\n" + "="*50)
print("GROUP COMPARISON:")
print("="*50)
print(f"Control Mean: {sum(control)/len(control):.2f}")
print(f"Intervention Mean: {sum(intervention)/len(intervention):.2f}")
print(f"\n{t_result.interpretation}")
EOF

python3 my_analysis.py
```

---

## 🔧 Troubleshooting

### **Problem: "command not found"**

**Solution:** You're trying to run Windows commands in Linux. Use:
- `python3` instead of `python`
- `bash script.sh` instead of `script.bat`
- Forward slashes `/` instead of backslashes `\`

### **Problem: "can't open file"**

**Solution:** Check your current directory:
```bash
pwd                      # Show current directory
ls -la                   # List files in current directory
cd ~/life-research-platform  # Go to project directory
```

### **Problem: "No module named 'research_data_library'"**

**Solution:** Ensure files are in the same directory:
```bash
cd ~/life-research-platform
ls -la *.py              # Should show all .py files
```

### **Problem: Import errors**

**Solution:** Files are in the current directory:
```bash
# In Python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from research_data_library import initialize_research_library
```

---

## 📦 File Management in Cloud Shell

### **List Files**
```bash
ls -la ~/life-research-platform
```

### **View File Contents**
```bash
cat test_library.py
head -20 research_data_library.py
```

### **Download Results**
```bash
# Click Upload/Download icon, select Download
# Or use Azure Storage commands
```

### **Check Disk Space**
```bash
df -h
du -sh ~/life-research-platform
```

---

## 🎯 Common Use Cases

### **Use Case 1: Quick EEG Analysis**

```bash
python3 << 'EOF'
from research_data_library import initialize_research_library
import random

library = initialize_research_library()
raw_eeg = [random.uniform(10, 30) for _ in range(256)]
result = library.process_raw_eeg(raw_eeg, sampling_rate=256)

print(f"Engagement: {result['engagement']:.3f}")
print(f"Focus: {result['focus']:.3f}")
EOF
```

### **Use Case 2: Statistical Comparison**

```bash
python3 << 'EOF'
from research_data_library import initialize_research_library

library = initialize_research_library()
control = [65, 68, 72, 70, 71, 69, 73]
intervention = [78, 82, 79, 85, 81, 83, 80]

result = library.calculate_t_test(control, intervention)
print(result.interpretation)
EOF
```

### **Use Case 3: Batch Processing**

```bash
python3 << 'EOF'
from research_data_library import initialize_research_library
import random

library = initialize_research_library()

for session in range(10):
    raw_eeg = [random.uniform(10, 30) for _ in range(256)]
    result = library.process_raw_eeg(raw_eeg, sampling_rate=256)
    print(f"Session {session+1}: Engagement={result['engagement']:.3f}")
EOF
```

---

## 📚 Additional Resources

### **View Documentation**
```bash
# View quick reference
cat RESEARCH_DATA_LIBRARY_QUICK_REF.txt

# View full documentation (if uploaded)
cat RESEARCH_DATA_LIBRARY_COMPLETE.md
```

### **Check Library Version**
```bash
python3 << 'EOF'
from research_data_library import initialize_research_library
library = initialize_research_library()
print(f"Library Version: {library.version}")
EOF
```

### **Get Help**
```bash
python3 << 'EOF'
from research_data_library import initialize_research_library
help(initialize_research_library)
EOF
```

---

## ✅ Verification Checklist

After deployment, verify everything works:

- [ ] Files uploaded to Cloud Shell
- [ ] Python 3.8+ available (`python3 --version`)
- [ ] Can import library (`from research_data_library import initialize_research_library`)
- [ ] EEG processing works (run test_library.py)
- [ ] Statistical analysis works
- [ ] Can populate full database
- [ ] Validation tests pass

---

## 🌐 Cloud Shell Session Management

**Important Notes:**
- Cloud Shell sessions timeout after **20 minutes** of inactivity
- Files in `~/` persist between sessions (stored in Azure Storage)
- Always save your work in the `~/life-research-platform` directory
- To reconnect: portal.azure.com → Click Cloud Shell icon

**Reconnect Commands:**
```bash
cd ~/life-research-platform
ls -la
python3 test_library.py  # Quick verification
```

---

## 🎓 Next Steps

Once deployed successfully:

1. **Run the full validation:**
   ```bash
   python3 validate_research_integration.py
   ```

2. **Populate the complete database:**
   ```bash
   python3 populate_research_database.py
   ```

3. **Create custom analysis scripts** for your research

4. **Integrate with Azure services** (Azure Functions, Storage, etc.)

---

## 📞 Support

If you encounter issues:

1. Check current directory: `pwd`
2. List available files: `ls -la`
3. Verify Python version: `python3 --version`
4. Check file permissions: `ls -l *.py`
5. View error details: Run with full traceback

---

**You're now ready to use the L.I.F.E. Research Platform in Azure Cloud Shell!** 🎉

Run `python3 test_library.py` to get started.
