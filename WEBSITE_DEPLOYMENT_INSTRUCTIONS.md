# L.I.F.E. Platform - Website Deployment Instructions
# Upload these files to your lifecoach-121.com web server

## FILES TO UPLOAD TO YOUR WEB SERVER:

### 1. Upload to: /privacy-policy/index.html
**File:** docs/privacy-policy.html
**URL Result:** https://lifecoach-121.com/privacy-policy/

### 2. Upload to: /terms-of-service/index.html  
**File:** docs/terms-of-service.html
**URL Result:** https://lifecoach-121.com/terms-of-service/

### 3. Upload to: /support/index.html
**File:** docs/support.html
**URL Result:** https://lifecoach-121.com/support/

### 4. Upload to: /api-docs/index.html
**File:** docs/api-docs.html  
**URL Result:** https://lifecoach-121.com/api-docs/

### 5. Upload to: /getting-started/index.html
**File:** docs/getting-started.html
**URL Result:** https://lifecoach-121.com/getting-started/

## DIRECTORY STRUCTURE ON YOUR WEB SERVER:
```
lifecoach-121.com/
├── privacy-policy/
│   └── index.html
├── terms-of-service/
│   └── index.html
├── support/
│   └── index.html
├── api-docs/
│   └── index.html
└── getting-started/
    └── index.html
```

## FTP/CPANEL UPLOAD INSTRUCTIONS:

1. **Login to your web hosting control panel** (cPanel, Plesk, or FTP)
2. **Navigate to public_html or www folder**
3. **Create these folders:**
   - privacy-policy/
   - terms-of-service/
   - support/
   - api-docs/
   - getting-started/
4. **Upload the HTML files as index.html in each folder**

## ALTERNATIVE: Upload as direct HTML files
If folder structure doesn't work, upload as:
- privacy-policy.html
- terms-of-service.html  
- support.html
- api-docs.html
- getting-started.html

Then URLs will be:
- https://lifecoach-121.com/privacy-policy.html
- https://lifecoach-121.com/terms-of-service.html
- etc.