# 💳 Partner Center - Payment Profile Setup Guide

**Date:** September 30, 2025  
**Issue:** "Account not publish eligible" - No payment profiles configured  
**Goal:** Create payout and tax profiles to enable offer publishing

---

## 🎯 **Quick Overview**

You need to create:
1. ✅ **Payment Profile** (bank account for receiving payments)
2. ✅ **Tax Profile** (W-8BEN for UK resident or W-9 for US resident)

**Time:** 15-20 minutes  
**Verification:** 1-3 business days

---

## 📋 **STEP 1: Create Payment Profile**

### **A. Click "Create payment profile" or "Add new profile"**

### **B. Fill Out Company/Individual Information**

**Profile type:**
- 🔘 **Individual** (if personal/sole trader)
- ⚪ Company (if limited company)

**Legal name:**
```
Sergio Paya Borrull
```
(Or your registered business name if you have a company)

**Country/Region:**
```
United Kingdom
```

**Address line 1:**
```
[Your street address]
```

**City:**
```
[Your city]
```

**Postal code:**
```
[Your postcode]
```

**Phone number:**
```
[Your phone number with country code]
```

**Email:**
```
sergio@lifecoach-121.com
```
(Or your preferred contact email)

---

### **C. Add Bank Account Details**

**Payment method:** Bank account (wire transfer)

**Bank country:** United Kingdom

**Bank name:**
```
[Your bank name - e.g., Barclays, HSBC, Lloyds, etc.]
```

**Account holder name:**
```
Sergio Paya Borrull
```
(Must match your bank account exactly)

**Account number:**
```
[Your 8-digit UK account number]
```

**Sort code:**
```
[Your 6-digit UK sort code - format: 12-34-56]
```

**IBAN (if available):**
```
GB[2 digits][4 letters][14 digits]
```
(UK IBANs start with GB - optional but recommended)

**SWIFT/BIC code:**
```
[Your bank's SWIFT code - 8 or 11 characters]
```
(e.g., BARCGB22 for Barclays)

**Bank address:**
```
[Your bank branch address]
```

---

### **D. Currency**

**Preferred payout currency:**
```
GBP - British Pound Sterling
```
(Or USD if you prefer, but GBP recommended for UK bank)

---

### **E. Save Payment Profile**

Click **"Save"** or **"Submit"**

---

## 🧾 **STEP 2: Create Tax Profile**

After saving payment profile, you need to add tax information:

### **A. Click "Add tax profile" or go to Tax Profile section**

### **B. Select Tax Residency**

**Country of tax residency:**
```
United Kingdom
```

**Taxpayer type:**
- 🔘 **Individual** (if personal)
- ⚪ Business (if limited company)

---

### **C. Complete W-8BEN Form (For Non-US Residents)**

Since you're UK-based, you'll fill out **Form W-8BEN** (Certificate of Foreign Status):

**Part I: Identification of Beneficial Owner**

**1. Name of individual:**
```
Sergio Paya Borrull
```

**2. Country of citizenship:**
```
United Kingdom
```
(Or your actual citizenship country)

**3. Permanent residence address:**
```
[Your UK address - same as payment profile]
```

**4. Mailing address (if different):**
```
[Leave blank if same as permanent address]
```

---

**Part II: Claim of Tax Treaty Benefits (UK-US Tax Treaty)**

**9. Country of tax residence:**
```
United Kingdom
```

**10. Tax identification number (TIN):**
```
[Your UK UTR number - Unique Taxpayer Reference]
```

**Where to find UTR:**
- On your Self Assessment tax return
- On HMRC letters
- Format: 10 digits (e.g., 1234567890)
- If you don't have one: Apply at gov.uk/apply-for-self-assessment-tax-return

**Alternative: National Insurance Number**
```
[Your NI number - format: AB123456C]
```
(If you don't have UTR yet)

---

**11. Reference number(s) (if applicable):**
```
[Leave blank unless you have one]
```

---

**Part III: Certification**

- ☑️ I certify that I am the beneficial owner
- ☑️ I am a resident of the United Kingdom
- ☑️ I am claiming treaty benefits under the US-UK tax treaty

**Signature:**
```
[Type your name: Sergio Paya Borrull]
```

**Date:**
```
September 30, 2025
```

---

### **D. Tax Treaty Benefits (Reduces Withholding)**

**Claim tax treaty benefits:** Yes ✅

**Article number:** Article 12 (Royalties)

**Rate of withholding:** 0% (UK-US treaty reduces from 30% to 0% for royalties/services)

This means Microsoft won't withhold US taxes on your marketplace earnings!

---

### **E. Save Tax Profile**

Click **"Submit"** or **"Save"**

---

## ✅ **What Happens Next**

### **After Submission:**

1. **Payment profile:** 
   - Microsoft verifies bank account details
   - May send test deposit (£0.01-£0.50)
   - Verification: 1-3 business days

2. **Tax profile:**
   - Microsoft reviews W-8BEN form
   - Usually approved within 24 hours
   - Sometimes immediate

### **Email Notifications:**
- ✅ "Payment profile verified"
- ✅ "Tax profile approved"
- ✅ "Your account is now publish eligible"

---

## 🚨 **Common Issues & Solutions**

### **Issue: "Invalid bank account"**
**Solution:** 
- Double-check account number and sort code
- Ensure account holder name matches exactly
- Try adding IBAN (convert at iban.com/calculate)

### **Issue: "UTR number not found"**
**Solutions:**
1. Use National Insurance number instead
2. Apply for UTR at gov.uk (takes 10 days)
3. Contact Partner Center support for alternative

### **Issue: "Address verification failed"**
**Solution:**
- Ensure address matches your bank account
- Use official address format (no abbreviations)
- Match address on government ID/utility bills

---

## 📞 **Need Help?**

### **Find Your Bank Details:**

**Barclays customers:**
- Login to online banking
- Go to "Account details"
- Find: Account number, Sort code, IBAN, SWIFT (BARCGB22)

**HSBC customers:**
- Login to online banking
- "View account details"
- SWIFT code: HSBCGB2L

**Lloyds customers:**
- Online banking → "Account information"
- SWIFT code: LOYDGB2L

**Other banks:**
- Call your bank or check online banking
- Request: Account number, Sort code, IBAN, SWIFT/BIC

---

### **Find Your UTR (Unique Taxpayer Reference):**

**If registered for Self Assessment:**
- Check HMRC letters
- Login to gov.uk Personal Tax Account
- Format: 10 digits

**If not registered:**
- You can use National Insurance number instead
- Or apply at: gov.uk/apply-for-self-assessment-tax-return
- Processing time: 10 working days (too slow for October 7)

**Recommendation:** Use NI number for now, add UTR later

---

## ⚡ **Expedite Verification**

### **Contact Partner Center Support:**

After submitting profiles:

1. Go to **Help + Support** in Partner Center
2. Click **"Create support ticket"**
3. Category: **"Payout and Tax"**
4. Subject: **"Expedite payment/tax profile verification - October 7 deadline"**
5. Details:
```
I have submitted payment profile (UK bank account) and tax profile (W-8BEN) 
on September 30, 2025. I have a critical marketplace offer launch scheduled 
for October 7, 2025. Can you please expedite the verification process?

Offer ID: life-theory
Profile name: Sergio Paya Borrull
Submission date: 30/09/2025

Thank you for your assistance.
```

**Phone (faster):** +1-800-PARTNER or UK support line

---

## 📊 **Timeline**

| Date | Action | Status |
|------|--------|--------|
| **Sep 30** | Submit payment & tax profiles | ✅ TODAY |
| **Oct 1** | Microsoft verifies bank account | Waiting |
| **Oct 1-2** | Profiles approved | Waiting |
| **Oct 3** | Account publish eligible | ✅ |
| **Oct 3-4** | Complete offer sections | Ready |
| **Oct 4-5** | Submit for certification | Ready |
| **Oct 5-7** | Microsoft certification (1-3 days) | Waiting |
| **Oct 7** | **PUBLISHED & LIVE** | 🚀 |

**Critical path:** Payment/tax verification must complete by Oct 2-3 for Oct 7 launch

---

## 🎯 **After Profiles Are Approved**

Once you see **"Publish eligible"** status:

1. ✅ Complete your 3 pricing plans
2. ✅ Finish Offer Listing (upload screenshots/logo)
3. ✅ Complete Preview Audience section
4. ✅ Complete Resell through CSPs section
5. ✅ Click "Review and Publish"
6. ✅ Submit for Microsoft certification

---

## 📋 **Quick Checklist**

- [ ] Create payment profile with UK bank details
- [ ] Add bank account (account number, sort code, SWIFT)
- [ ] Submit payment profile
- [ ] Create tax profile (W-8BEN for UK resident)
- [ ] Enter UTR or National Insurance number
- [ ] Claim UK-US tax treaty benefits (0% withholding)
- [ ] Submit tax profile
- [ ] Wait for verification emails (1-3 days)
- [ ] Optional: Contact support to expedite
- [ ] Check for "Publish eligible" status

---

## 💡 **Pro Tips**

1. **Use your primary bank account** - Makes verification faster
2. **Double-check all details** - Typos cause delays
3. **Enable email notifications** - Get updates immediately
4. **Have documents ready** - Bank statement, tax documents
5. **Submit early in the day** - Gets reviewed faster
6. **Contact support** - Request expedited review for October 7 deadline

---

## 🚀 **START NOW**

1. Click **"Create payment profile"** in Partner Center
2. Fill in your UK bank account details
3. Submit payment profile
4. Click **"Add tax profile"**
5. Complete W-8BEN form with UTR/NI number
6. Submit tax profile
7. **Tell me when done** so I can help with next steps!

---

**Need help finding your bank details or UTR?** Let me know and I'll guide you! 📞
