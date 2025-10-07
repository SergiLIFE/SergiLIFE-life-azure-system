# PARTNER CENTER URL FIX GUIDE
## Fix Non-Operational Support URL Issue

**Date:** October 2, 2025  
**Issue:** `https://lifecoach121.com/support` is not operational  
**Impact:** Blocking Partner Center publish eligibility

---

## 🚨 CRITICAL: URLs to Fix in Partner Center

### **Section 1: Offer Listing**

Navigate to: **Offer Listing** section in Partner Center

**Fields to Update:**

1. **Support URL / Support Link:**
   - ❌ REMOVE: `https://lifecoach121.com/support`
   - ✅ USE: `https://lifecoach-121.com`

2. **Support Email:**
   - ✅ USE: `sergi@lifecoach-121.com`

3. **Support Contact:**
   - ✅ USE: `sergi@lifecoach-121.com`

### **Section 2: Technical Configuration**

Navigate to: **Technical Configuration** section

**Fields to Update:**

1. **Support URL:**
   - ❌ REMOVE: `https://lifecoach121.com/support`
   - ✅ USE: `https://lifecoach-121.com`

2. **Landing Page URL:**
   - ✅ VERIFY: `https://lifecoach-121.com` (should be working)

3. **Connection Webhook URL:**
   - ✅ VERIFY: Azure Function URL is correct

### **Section 3: CSP Marketing Materials**

Navigate to: **Offer Listing** → CSP Program Marketing Materials URL

**Field to Update:**

1. **CSP Program Marketing Materials URL:**
   - ✅ USE: `https://lifecoach-121.com`

### **Section 4: Properties**

Navigate to: **Properties** section

**Fields to Verify:**

1. **Support Contact Information:**
   - ✅ USE: Email only (`sergi@lifecoach-121.com`)
   - ✅ OR: Main website (`https://lifecoach-121.com`)

---

## 🔍 Complete URL Audit Checklist

Go through your entire Partner Center offer and replace ANY instance of:

### ❌ REMOVE These URLs:
- `https://lifecoach121.com/support`
- `http://lifecoach121.com/support`
- Any `/support` path that's not operational

### ✅ REPLACE With:
- **Main Website:** `https://lifecoach-121.com`
- **Support Email:** `sergi@lifecoach-121.com`
- **Portal:** `https://lifecoach-121.com` (if different from main)

---

## 📋 Step-by-Step Fix Process

### Step 1: Offer Listing
1. Go to Partner Center → Your offer → **Offer listing**
2. Find "Support URL" or "Support link" field
3. Change to: `https://lifecoach-121.com`
4. Update "Support email" to: `sergi@lifecoach-121.com`
5. Click **"Save draft"**

### Step 2: Technical Configuration
1. Go to **Technical configuration**
2. Find "Support URL" field
3. Change to: `https://lifecoach-121.com`
4. Verify "Landing page URL" is: `https://lifecoach-121.com`
5. Click **"Save draft"**

### Step 3: CSP Marketing Materials
1. Go to **Offer listing**
2. Scroll to "CSP Program Marketing Materials URL"
3. Enter: `https://lifecoach-121.com`
4. Click **"Save draft"**

### Step 4: Properties
1. Go to **Properties**
2. Check "Support contact" section
3. Use email: `sergi@lifecoach-121.com`
4. Click **"Save draft"**

### Step 5: All Plans
1. Check **each plan** (Basic, Pro, Enterprise)
2. Verify no support URLs are broken
3. Save all plans

### Step 6: Review and Validate
1. Go to **Review and publish**
2. Check for validation errors
3. Look for URL-related warnings
4. Fix any remaining issues

---

## ✅ Working URLs You CAN Use

These URLs are verified working:

1. **Main Website:**
   ```
   https://lifecoach-121.com
   ```

2. **Support Email:**
   ```
   sergi@lifecoach-121.com
   ```

3. **Technical Email:**
   ```
   sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com
   ```

4. **Azure Function (Health Check):**
   ```
   https://func-life-platform-prod.azurewebsites.net/api/health
   ```

---

## 🔧 Optional: Create Support Page

If you want to make `https://lifecoach-121.com/support` operational, you need to:

1. Create a simple HTML support page
2. Upload to your web hosting
3. Test the URL works
4. Update Partner Center with the working URL

**Example Support Page Content:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>L.I.F.E Platform Support</title>
</head>
<body>
    <h1>L.I.F.E Platform Support</h1>
    <h2>Contact Information</h2>
    <p><strong>Email:</strong> sergi@lifecoach-121.com</p>
    <p><strong>Response Time:</strong> Within 2 hours (business hours GMT)</p>
    <h2>Technical Support</h2>
    <p><strong>Email:</strong> sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com</p>
    <h2>Company</h2>
    <p>L.I.F.ECoach121.com Limited</p>
    <p>UK Seller ID: 92230950</p>
</body>
</html>
```

Save this as `support.html` and upload to your website's `/support` directory.

---

## 🚀 After Fixing URLs

1. **Save all changes** in Partner Center
2. **Wait 1-2 hours** for validation to re-run
3. **Check "Review and publish"** for errors
4. If no errors → **Submit for certification**

---

## ⏰ Updated Timeline

- **Today (Oct 2):** Fix all URLs, save drafts
- **Oct 3-4:** Wait for 48-hour payout/tax sync + URL validation
- **Oct 4-5:** Submit for certification
- **Oct 7:** LAUNCH! 🎂

---

## 📞 If Still Blocked After URL Fix

Contact Partner Center Support:
1. Click **"Help"** (? icon)
2. Select **"Contact support"**
3. Topic: **"URL validation blocking publish"**
4. Message: **"Fixed non-operational support URL. All URLs now verified working. Request manual review for Seller ID 92230950."**

---

**IMMEDIATE ACTION: Go through Partner Center and replace ALL instances of `/support` URL with main website or email!** ✅
