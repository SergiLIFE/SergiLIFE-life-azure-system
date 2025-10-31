# DNS Configuration Guide for lifecoach-121.com
## Deploying L.I.F.E. Platform to Your Custom Domain

---

## Current Status
- ✅ **HTML File Deployed:** `docs/life-theory-platform.html` is live on GitHub
- ✅ **GitHub Pages Enabled:** Repository configured for deployment
- ✅ **CNAME File Created:** `docs/CNAME` contains `lifecoach-121.com`
- ⏳ **DNS Configuration Needed:** Follow steps below

---

## Step-by-Step DNS Configuration

### Step 1: Log Into Your Domain Registrar

Your domain `lifecoach-121.com` is registered somewhere (GoDaddy, Namecheap, Cloudflare, etc.).

**Find your registrar:**
1. Go to https://who.is
2. Enter: `lifecoach-121.com`
3. Check the "Registrar" field
4. Log into that registrar's website

---

### Step 2: Navigate to DNS Management

Once logged in:
1. Find **DNS Settings** or **DNS Management** or **Manage DNS**
2. Locate your domain: `lifecoach-121.com`
3. Click **Manage** or **Edit DNS Records**

---

### Step 3: Add DNS Records

You need to add **ONE** of the following configurations (choose Option A or Option B):

---

#### **Option A: CNAME Record (Recommended - Simpler)**

**If your domain is at the ROOT level (lifecoach-121.com):**

⚠️ Some registrars don't allow CNAME at root. If this fails, use Option B instead.

| Type  | Name/Host | Value/Target                          | TTL  |
|-------|-----------|---------------------------------------|------|
| CNAME | @         | sergilife.github.io                   | 3600 |

**OR if you want to use www subdomain (www.lifecoach-121.com):**

| Type  | Name/Host | Value/Target                          | TTL  |
|-------|-----------|---------------------------------------|------|
| CNAME | www       | sergilife.github.io                   | 3600 |

---

#### **Option B: A Records (Most Compatible)**

**Add FOUR A records pointing to GitHub Pages IP addresses:**

| Type | Name/Host | Value/Target      | TTL  |
|------|-----------|-------------------|------|
| A    | @         | 185.199.108.153   | 3600 |
| A    | @         | 185.199.109.153   | 3600 |
| A    | @         | 185.199.110.153   | 3600 |
| A    | @         | 185.199.111.153   | 3600 |

**PLUS add CNAME for www (optional but recommended):**

| Type  | Name/Host | Value/Target                          | TTL  |
|-------|-----------|---------------------------------------|------|
| CNAME | www       | sergilife.github.io                   | 3600 |

---

### Step 4: Remove Conflicting Records

**IMPORTANT:** Remove any existing A or CNAME records for `@` or `www` that point elsewhere.

**Common conflicts to delete:**
- Old A records pointing to different IPs
- CNAME records pointing to old hosting providers
- Redirects or parking page records

---

### Step 5: Save DNS Changes

1. Click **Save** or **Save Changes** or **Update DNS**
2. DNS propagation takes **5-60 minutes** (sometimes up to 24 hours globally)

---

## Verify DNS Configuration

### Method 1: Command Line Check (Windows CMD)

```cmd
nslookup lifecoach-121.com
```

**Expected output (after propagation):**
```
Name:    lifecoach-121.com
Addresses:  185.199.108.153
            185.199.109.153
            185.199.110.153
            185.199.111.153
```

### Method 2: Online DNS Checker

Visit: https://dnschecker.org

1. Enter: `lifecoach-121.com`
2. Select: **A** record
3. Click **Search**
4. Wait for global propagation (green checkmarks worldwide)

---

## Enable HTTPS (After DNS Propagates)

### Step 1: Wait for DNS Validation

1. Go to: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/pages
2. Wait for **green checkmark** next to "DNS check is in progress"
3. This means GitHub has verified your DNS configuration

### Step 2: Enable HTTPS

Once DNS shows ✅:
1. On the same GitHub Pages settings page
2. Check the box: **"Enforce HTTPS"**
3. Click **Save**
4. Wait 5-10 minutes for SSL certificate provisioning

---

## Your Final URLs

After DNS propagation and HTTPS enablement:

| URL Type          | Address                                                          | Status       |
|-------------------|------------------------------------------------------------------|--------------|
| **Custom Domain** | https://lifecoach-121.com/life-theory-platform.html              | ⏳ DNS Setup |
| **Custom (www)**  | https://www.lifecoach-121.com/life-theory-platform.html          | ⏳ DNS Setup |
| **GitHub Pages**  | https://sergilife.github.io/SergiLIFE-life-azure-system/life-theory-platform.html | ✅ Live Now  |

---

## Troubleshooting

### Issue: "DNS check failed"

**Solution:**
1. Verify A records point to correct GitHub IPs
2. Wait 15 more minutes (DNS takes time)
3. Clear DNS cache on your computer:
   ```cmd
   ipconfig /flushdns
   ```

### Issue: "404 Not Found" on custom domain

**Solution:**
1. Check `docs/CNAME` file contains exactly: `lifecoach-121.com`
2. Re-enable GitHub Pages if it disabled itself:
   - Go to Settings → Pages
   - Source: Deploy from branch → main → /docs
   - Custom domain: lifecoach-121.com
   - Click Save

### Issue: "Certificate error" or "Not secure"

**Solution:**
1. Wait for DNS validation to complete (green checkmark)
2. Enable "Enforce HTTPS" in GitHub Pages settings
3. Wait 5-10 minutes for certificate provisioning
4. Hard refresh browser (Ctrl+F5)

### Issue: Changes take forever

**DNS propagation is slow by design:**
- Your ISP: 5-30 minutes
- Your country: 30-60 minutes
- Worldwide: Up to 24 hours

**Speed it up:**
1. Change DNS TTL to 300 seconds (5 minutes) instead of 3600
2. Use Google DNS: https://developers.google.com/speed/public-dns/docs/using
3. Test from different network (mobile hotspot)

---

## Quick Start Commands

### Check Current DNS Status
```cmd
nslookup lifecoach-121.com
nslookup www.lifecoach-121.com
```

### Test GitHub Pages URL (Should Work Now)
```cmd
curl https://sergilife.github.io/SergiLIFE-life-azure-system/life-theory-platform.html
```

### Open GitHub Pages Settings
```cmd
start https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/pages
```

### Open Live Platform
```cmd
start https://sergilife.github.io/SergiLIFE-life-azure-system/life-theory-platform.html
```

---

## Example DNS Configuration (Cloudflare)

If using **Cloudflare**:

1. Log in to https://dash.cloudflare.com
2. Select domain: `lifecoach-121.com`
3. Click **DNS** in left sidebar
4. Click **Add record**
5. Add these records:

```
Type: A
Name: @
IPv4 address: 185.199.108.153
Proxy status: DNS only (gray cloud)
TTL: Auto

(Repeat for other 3 IPs: .109, .110, .111)

Type: CNAME
Name: www
Target: sergilife.github.io
Proxy status: DNS only (gray cloud)
TTL: Auto
```

6. Click **Save**

---

## Example DNS Configuration (GoDaddy)

If using **GoDaddy**:

1. Log in to https://account.godaddy.com
2. Click **My Products**
3. Find `lifecoach-121.com` → Click **DNS**
4. Click **Add** button
5. Add these records:

```
Type: A
Name: @
Value: 185.199.108.153
TTL: 1 Hour

(Click Add 3 more times for .109, .110, .111)

Type: CNAME
Name: www
Value: sergilife.github.io
TTL: 1 Hour
```

6. Click **Save**

---

## Summary Checklist

- [ ] Logged into domain registrar
- [ ] Navigated to DNS management
- [ ] Added 4 A records (185.199.108/109/110/111.153)
- [ ] Added CNAME for www → sergilife.github.io
- [ ] Removed conflicting old records
- [ ] Saved DNS changes
- [ ] Waited 15-60 minutes for propagation
- [ ] Verified with `nslookup lifecoach-121.com`
- [ ] Checked GitHub Pages settings (green checkmark)
- [ ] Enabled "Enforce HTTPS"
- [ ] Tested https://lifecoach-121.com/life-theory-platform.html

---

## Support Resources

- **GitHub Pages Custom Domain Docs:** https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
- **DNS Checker Tool:** https://dnschecker.org
- **GitHub Pages Status:** https://www.githubstatus.com
- **Your Repository Settings:** https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/pages

---

## Contact Information

**L.I.F.E. Platform - October 31, 2025 Deployment**  
**Author:** Sergio Paya Borrull  
**Offer ID:** 9a600d96-fe1e-420b-902a-a0c42c561adb  
**Repository:** https://github.com/SergiLIFE/SergiLIFE-life-azure-system

---

**🎯 Expected Timeline:**
- **Now:** GitHub Pages URL works immediately
- **5-30 minutes:** DNS propagates to your ISP
- **30-60 minutes:** DNS propagates nationally
- **1-24 hours:** Full global DNS propagation
- **After DNS:** HTTPS certificate auto-provisions (5-10 min)

**Your platform is already live at the GitHub Pages URL!**  
The custom domain is just an additional alias for convenience.
