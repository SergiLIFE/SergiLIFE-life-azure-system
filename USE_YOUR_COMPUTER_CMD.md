# 💻 USE YOUR COMPUTER CMD - NOT VS CODE TERMINAL

Since VS Code terminal isn't working, use your computer's CMD directly. Here's exactly how:

---

## ✅ STEP 1: Open Command Prompt on Your Computer

### **Windows 10/11:**
1. Click **Windows Start Button** (bottom left)
2. Type: `cmd`
3. Press **Enter**

### **OR Press These Keys:**
- **Windows Key + R** 
- Type: `cmd`
- Press **Enter**

### **You should see:**
```
C:\Users\Sergio Paya Borrull>
```

✅ **CMD is now open!**

---

## ✅ STEP 2: Copy This Entire Command

```cmd
cd "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system" && python -m http.server 8080
```

---

## ✅ STEP 3: Paste Into CMD

1. In CMD window, right-click
2. Click **Paste**
3. Press **Enter**

### **You should see:**
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

✅ **Server is running!**

---

## ✅ STEP 4: Open Browser

**Open ANY web browser** (Chrome, Edge, Firefox, etc.) and go to:

```
http://localhost:8080/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
```

### **You should see:**
- L.I.F.E Platform loads
- Blue header
- Dashboard with metrics
- All buttons clickable

✅ **PLATFORM IS RUNNING!**

---

## 📱 Try Other Platforms

Once you have the server running, you can click any of these:

```
http://localhost:8080/L.I.F.E_PLATFORM_ULTIMATE_INTEGRATED.html
http://localhost:8080/LIFE_AI_PLATFORM_REAL.html
http://localhost:8080/LIFE_ENTERPRISE_PLATFORM_REAL.html
http://localhost:8080/LIFE_EDUCATION_PLATFORM_REAL.html
http://localhost:8080/LIFE_RESEARCH_PLATFORM_REAL.html
```

---

## 🛑 To Stop the Server

In CMD window, press: **Ctrl + C**

```
C:\Users\...\SergiLIFE-life-azure-system>Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
^C
Keyboard interrupt received, exiting.
```

✅ Server stopped!

---

## ❌ If Something Doesn't Work

### **Error: "python not found"**

Try this instead:
```cmd
cd "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system" && python3 -m http.server 8080
```

### **Error: "Port 8080 already in use"**

Use a different port:
```cmd
cd "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system" && python -m http.server 8081
```

Then access: `http://localhost:8081/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html`

### **Nothing loads in browser**

1. Make sure CMD shows: `Serving HTTP on 0.0.0.0 port 8080`
2. Try refreshing browser: `F5` or `Ctrl + R`
3. Try different platform link from list above
4. Check your internet connection

---

## 📋 COMPLETE CHECKLIST

- [ ] CMD window open
- [ ] Command pasted and running
- [ ] See "Serving HTTP on 0.0.0.0 port 8080"
- [ ] Browser opened
- [ ] Pasted URL: `http://localhost:8080/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html`
- [ ] Platform loaded
- [ ] Can click buttons and tabs

✅ **All checked? You're done!**

---

## 🎯 NEXT STEPS

### **Test WITHOUT EEG (Right now):**
- Server is running ✅
- Platform loads ✅
- Everything works ✅
- **Done!**

### **Test WITH EEG (If available):**
1. Open **ANOTHER** CMD window (keep first one running)
2. Run:
   ```cmd
   cd "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system" && python life_eeg_server.py
   ```
3. Go back to first CMD window and platform is still running
4. Open same URL - now with real EEG data!

---

## ✅ YOU'RE READY!

**Your setup:**
- ✅ Using CMD on your computer
- ✅ Not using VS Code terminal
- ✅ All platforms accessible
- ✅ No VS Code required

**Just follow the steps above and you'll have all platforms running!**

---

## 🎉 SUMMARY

| Step | Action |
|------|--------|
| 1 | Open CMD (Windows Key + R → cmd → Enter) |
| 2 | Copy the command from STEP 2 |
| 3 | Right-click CMD → Paste |
| 4 | Press Enter |
| 5 | Wait for "Serving HTTP" message |
| 6 | Open browser to: `http://localhost:8080/[platform].html` |
| **DONE** | **Platform is running!** ✅ |

---

**Need help? Run the command and tell me what error you see!**
