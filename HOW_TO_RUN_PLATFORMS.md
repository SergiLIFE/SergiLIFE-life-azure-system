# 🎯 HOW TO RUN PLATFORMS - FROM HERE vs YOUR COMPUTER

## Option 1: Run FROM YOUR COMPUTER CMD (Recommended for Testing)

### **Step 1: Open Command Prompt**
```
Windows Key + R
Type: cmd
Press Enter
```

### **Step 2: Navigate to Project Folder**
```cmd
cd C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system
```

### **Step 3: Start Web Server**
```cmd
python -m http.server 8080
```

**You should see:**
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

### **Step 4: Open Browser**
```
http://localhost:8080/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
```

**Result:** ✅ Platform loads and runs on YOUR computer

---

## Option 2: Run FROM VS CODE INTEGRATED TERMINAL

### **Step 1: Open VS Code Terminal**
```
Ctrl + ` (backtick)
OR
View → Terminal
```

### **Step 2: Ensure You're in Project Directory**
```cmd
cd C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system
```

### **Step 3: Start Web Server**
```cmd
python -m http.server 8080
```

### **Step 4: Open Browser**
```
http://localhost:8080/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
```

**Result:** ✅ Same as Option 1, but terminal stays in VS Code

---

## Option 3: Run EEG Server (More Complex)

### **Terminal 1: Start EEG Server**
```cmd
cd C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system

python life_eeg_server.py
```

### **Terminal 2: Start Web Server** (open new terminal)
```cmd
cd C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system

python -m http.server 8080
```

### **Terminal 3: Open Browser**
```
http://localhost:8080/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
```

**Result:** ✅ Platform runs with real EEG data (if connected)

---

## ⚡ QUICK COMPARISON

| Method | Setup | Speed | Convenience | Best For |
|--------|-------|-------|-------------|----------|
| **CMD** | Open cmd manually | 1-2 min | Medium | Quick testing |
| **VS Code Terminal** | Ctrl+` | 1 min | High | While coding |
| **With EEG** | 3 terminals | 3-5 min | Medium | Full testing |

---

## 🚀 FASTEST WAY (RECOMMENDED)

### **Right Now:**

1. **Open Command Prompt** (Windows Key + R → cmd → Enter)
2. **Paste this entire command:**
```cmd
cd C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system && python -m http.server 8080
```
3. **Then open browser:**
```
http://localhost:8080/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
```

**Total time: 30 seconds** ✅

---

## 📋 ALL PLATFORMS (Copy & Paste Ready)

Once you have the server running, click ANY of these:

```
http://localhost:8080/L.I.F.E_PLATFORM_ULTIMATE_INTEGRATED.html
http://localhost:8080/LIFE_AI_PLATFORM_REAL.html
http://localhost:8080/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
http://localhost:8080/LIFE_ENTERPRISE_PLATFORM_REAL.html
http://localhost:8080/LIFE_EDUCATION_PLATFORM_REAL.html
http://localhost:8080/LIFE_RESEARCH_PLATFORM_REAL.html
```

---

## ✅ TROUBLESHOOTING

### **"Port 8080 is already in use"**
```cmd
python -m http.server 8081
REM Then use: http://localhost:8081/filename.html
```

### **"Python not found"**
```cmd
REM Try full path:
C:\Users\Sergio Paya Borrull\AppData\Local\Programs\Python\Python311\python.exe -m http.server 8080
```

### **Can't find folder**
```cmd
REM Copy this entire path:
C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system

REM Then: cd [paste-path]
```

---

## 🎯 WHICH SHOULD YOU USE?

### **For Quick Testing:** Use CMD ✅
- Independent of VS Code
- Easy to restart
- Simple setup

### **For Active Development:** Use VS Code Terminal ✅
- Everything in one window
- Can see code and test simultaneously
- Easy to stop/restart

### **For Full Testing:** Use Both ✅
- Terminal 1: EEG server
- Terminal 2: Web server  
- Terminal 3: Browser

---

## 📝 SUMMARY

**You can run from:**
- ✅ Your computer CMD (fastest, easiest)
- ✅ VS Code integrated terminal (convenient)
- ✅ Both (for EEG testing)

**All three work the same way!**

**Start now? Use this:**
```cmd
cd C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system && python -m http.server 8080
```

Then: `http://localhost:8080/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html`

Done! 🚀
