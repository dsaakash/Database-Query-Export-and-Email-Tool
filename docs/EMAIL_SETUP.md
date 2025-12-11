# Email Setup Guide - Gmail & Outlook

Step-by-step instructions for setting up email functionality.

## 📧 Email Features

- **TO Recipients** - Primary recipients (required)
- **CC Recipients** - Carbon copy recipients (optional)
- **Multiple Recipients** - Support for comma-separated email addresses
- **Attachments** - Excel and PDF file attachments
- **HTML Body** - Formatted HTML table in email body

## 📧 Gmail Setup

### Step-by-Step Instructions

#### Step 1: Enable 2-Step Verification

1. **Go to Google Account**
   - Visit: https://myaccount.google.com/
   - Sign in with your Gmail account

2. **Navigate to Security**
   - Click **Security** in the left sidebar
   - Or go directly: https://myaccount.google.com/security

3. **Enable 2-Step Verification**
   - Find **"2-Step Verification"** section
   - Click **Get Started** or **Turn On**
   - Follow the prompts:
     - Verify your phone number
     - Enter verification code sent to your phone
     - Confirm setup

#### Step 2: Generate App Password

1. **Go to App Passwords**
   - Still in Security settings
   - Click on **"2-Step Verification"** (the text link, not toggle)
   - Scroll down to **"App passwords"**
   - Click **"App passwords"**
   - You may need to sign in again

2. **Create App Password**
   - **Select app:** Choose **"Mail"**
   - **Select device:** Choose **"Other (Custom name)"**
   - Enter name: `Database Tool` or `Python Script`
   - Click **Generate**

3. **Copy the Password**
   - You'll see a 16-character password like: `abcd efgh ijkl mnop`
   - **IMPORTANT:** Copy this immediately - you won't see it again!
   - Remove spaces when using: `abcdefghijklmnop`

#### Step 3: Configure .env File

Create or edit `.env` file in project root:

```env
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**Replace:**
- `your_email@gmail.com` with your actual Gmail address
- `abcdefghijklmnop` with your 16-character app password (no spaces)

#### Visual Guide

```
Google Account → Security → 2-Step Verification → App Passwords
                                                      ↓
                                            Select: Mail
                                            Device: Other
                                            Name: Database Tool
                                                      ↓
                                            Generate → Copy Password
```

---

## 📧 Outlook Setup

### Step-by-Step Instructions

#### Step 1: Enable Two-Factor Authentication

1. **Go to Microsoft Account**
   - Visit: https://account.microsoft.com/security
   - Sign in with your Outlook/Microsoft account

2. **Enable Two-Step Verification**
   - Under **Security** section
   - Find **"Two-step verification"**
   - Click **Turn on** or **Set up**
   - Follow the prompts to complete setup

#### Step 2: Generate App Password

1. **Go to Advanced Security**
   - In Security page, click **"Advanced security options"**
   - Or go directly: https://account.microsoft.com/security

2. **Create App Password**
   - Scroll to **"App passwords"** section
   - Click **"Create a new app password"**
   - Give it a name: `Database Tool`
   - Click **Generate**

3. **Copy the Password**
   - You'll see a 16-character password like: `abcd-efgh-ijkl-mnop`
   - **IMPORTANT:** Copy this immediately - you won't see it again!
   - Remove dashes when using: `abcdefghijklmnop`

#### Step 3: Configure .env File

Create or edit `.env` file in project root:

```env
SMTP_USER=your_email@outlook.com
SMTP_PASSWORD=abcdefghijklmnop
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

**Replace:**
- `your_email@outlook.com` with your actual Outlook email
- `abcdefghijklmnop` with your 16-character app password (no dashes)

**Supported Outlook Domains:**
- `@outlook.com`
- `@hotmail.com`
- `@live.com`
- `@msn.com`

#### Visual Guide

```
Microsoft Account → Security → Advanced Security Options → App Passwords
                                                                    ↓
                                                          Create New
                                                          Name: Database Tool
                                                                    ↓
                                                          Generate → Copy Password
```

---

## ✅ Testing Your Email Setup

### Quick Test Script

Create a file `test_email.py`:

```python
import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

# Load from .env
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", "587"))

# Test email
try:
    yag = yagmail.SMTP(
        user=smtp_user,
        password=smtp_password,
        host=smtp_host,
        port=smtp_port
    )
    
    yag.send(
        to=smtp_user,  # Send to yourself for testing
        subject="Test Email from Database Tool",
        contents="If you receive this, your email setup is working correctly!"
    )
    
    print("✓ Test email sent successfully!")
    print(f"✓ Check your inbox: {smtp_user}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check .env file has correct values")
    print("2. Verify you're using App Password (not regular password)")
    print("3. Ensure 2-Step Verification is enabled")
```

Run the test:

```bash
python test_email.py
```

---

## 🔍 Troubleshooting

### Common Issues

#### "Authentication failed" or "Invalid credentials"

**Gmail:**
- ✅ Using App Password (not regular password)?
- ✅ 2-Step Verification enabled?
- ✅ Removed spaces from app password?
- ✅ Correct email address?

**Outlook:**
- ✅ Using App Password (not regular password)?
- ✅ Two-Factor Authentication enabled?
- ✅ Removed dashes from app password?
- ✅ Correct email address?

#### "Less secure app access" (Gmail)

**Solution:**
- This means you're using your regular password
- You **MUST** use an App Password instead
- App Passwords are the only way for Gmail now

#### "Connection refused"

**Solutions:**
1. Check internet connection
2. Verify SMTP settings:
   - Gmail: `smtp.gmail.com:587`
   - Outlook: `smtp-mail.outlook.com:587`
3. Check firewall settings
4. Try from different network

#### "App password not working"

**Solutions:**
1. Regenerate app password
2. Make sure you copied the full 16 characters
3. Remove all spaces/dashes
4. Verify 2-Step Verification is still enabled

---

## 📋 Quick Reference

### Gmail Configuration

```env
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=16_char_app_password_no_spaces
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**Setup Steps:**
1. Enable 2-Step Verification
2. Generate App Password
3. Copy 16-character password
4. Add to .env (remove spaces)

### Outlook Configuration

```env
SMTP_USER=your_email@outlook.com
SMTP_PASSWORD=16_char_app_password_no_dashes
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

**Setup Steps:**
1. Enable Two-Factor Authentication
2. Generate App Password
3. Copy 16-character password
4. Add to .env (remove dashes)

---

## 🎯 Key Points to Remember

1. **Always use App Passwords** - Never use your regular email password
2. **2-Step Verification Required** - Must be enabled before generating app password
3. **Remove Formatting** - Remove spaces (Gmail) or dashes (Outlook) from app password
4. **Keep it Secret** - Never share your app password or commit .env to version control
5. **One App Password** - You can reuse the same app password for multiple scripts

---

## 📞 Still Having Issues?

1. **Double-check .env file:**
   - No extra spaces
   - Correct email address
   - App password (not regular password)

2. **Verify 2-Step Verification:**
   - Gmail: https://myaccount.google.com/security
   - Outlook: https://account.microsoft.com/security

3. **Test with simple script:**
   - Use the test_email.py script above
   - Check error messages carefully

4. **Regenerate App Password:**
   - Delete old one
   - Create new one
   - Update .env file

---

**Need more help?** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete documentation.

