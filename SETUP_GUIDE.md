# Complete Setup and Usage Guide

This guide will walk you through setting up and running the Database Query, Export, and Email Tool.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Email Setup](#email-setup)
   - [Gmail SMTP Setup](#gmail-smtp-setup)
   - [Outlook SMTP Setup](#outlook-smtp-setup)
4. [Running the Application](#running-the-application)
5. [Usage Examples](#usage-examples)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed on your system
- **pip** (Python package installer)
- **Internet connection** (for installing packages and sending emails)
- **Database access** (Oracle, PostgreSQL, or SQLite database)

### Check Python Version

```bash
python3 --version
# Should show Python 3.8 or higher
```

---

## Installation

### Step 1: Navigate to Project Directory

```bash
cd "/Users/aakash/Desktop/My workspace/oracle_db_connection"
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt after activation.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data manipulation)
- openpyxl (Excel export)
- python-dotenv (environment variables)
- oracledb (Oracle database)
- yagmail (email sending)
- reportlab (PDF export)
- psycopg2-binary (PostgreSQL)
- sqlalchemy (database abstraction)

### Step 4: Verify Installation

```bash
python3 -c "import pandas, openpyxl, yagmail, reportlab; print('✓ All packages installed successfully')"
```

---

## Email Setup

The application supports sending emails via Gmail or Outlook. You need to configure SMTP settings in a `.env` file.

### Create .env File

Create a file named `.env` in the project root directory:

```bash
touch .env
```

Or create it manually in your text editor.

---

## Gmail SMTP Setup

### Step 1: Enable 2-Step Verification

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", find **2-Step Verification**
4. Click **Get Started** and follow the prompts to enable 2-Step Verification
   - You'll need to verify your phone number
   - Google will send a verification code

### Step 2: Generate App Password

1. Still in **Security** settings, scroll down to find **2-Step Verification**
2. Click on **2-Step Verification** (not the toggle, but the text link)
3. Scroll down to find **App passwords**
4. Click on **App passwords**
   - You may need to sign in again
5. Select app: Choose **Mail**
6. Select device: Choose **Other (Custom name)**
   - Enter a name like "Database Tool" or "Python Script"
7. Click **Generate**
8. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)
   - You won't be able to see it again!
   - Remove spaces when using it (e.g., `abcdefghijklmnop`)

### Step 3: Configure .env File

Add the following to your `.env` file:

```env
# Gmail SMTP Configuration
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**Important Notes:**
- Use your **full Gmail address** (e.g., `john.doe@gmail.com`)
- Use the **16-character app password** (not your regular Gmail password)
- Remove spaces from the app password
- Keep the `.env` file secure and never commit it to version control

### Step 4: Test Gmail Configuration

You can test your Gmail setup with this Python script:

```python
import yagmail

# Test email
yag = yagmail.SMTP(
    user="your_email@gmail.com",
    password="your_app_password",
    host="smtp.gmail.com",
    port=587
)

yag.send(
    to="your_email@gmail.com",  # Send to yourself for testing
    subject="Test Email",
    contents="This is a test email from the database tool."
)

print("✓ Test email sent successfully!")
```

---

## Outlook SMTP Setup

### Method 1: Using App Password (Recommended)

#### Step 1: Enable Two-Factor Authentication

1. Go to [Microsoft Account Security](https://account.microsoft.com/security)
2. Sign in with your Outlook/Microsoft account
3. Under **Security**, find **Advanced security options**
4. Enable **Two-step verification** if not already enabled
   - Follow the prompts to set it up

#### Step 2: Generate App Password

1. Go to [Microsoft Account Security](https://account.microsoft.com/security)
2. Click on **Advanced security options**
3. Under **App passwords**, click **Create a new app password**
4. Give it a name like "Database Tool"
5. Click **Generate**
6. **Copy the 16-character password** (it will look like: `abcd-efgh-ijkl-mnop`)
   - You won't be able to see it again!
   - Remove dashes when using it (e.g., `abcdefghijklmnop`)

#### Step 3: Configure .env File

Add the following to your `.env` file:

```env
# Outlook SMTP Configuration
SMTP_USER=your_email@outlook.com
SMTP_PASSWORD=abcdefghijklmnop
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

**Important Notes:**
- Use your **full Outlook email address** (e.g., `john.doe@outlook.com` or `john.doe@hotmail.com`)
- Use the **16-character app password** (not your regular password)
- Remove dashes from the app password
- Works with: `@outlook.com`, `@hotmail.com`, `@live.com`, `@msn.com`

### Method 2: Using OAuth2 (Advanced)

For enterprise/Office 365 accounts, you may need OAuth2. This is more complex and typically requires additional setup. For most users, the App Password method above works fine.

---

## Running the Application

### Basic Usage

1. **Activate virtual environment** (if not already active):
   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Follow the interactive prompts**:
   - Select database type (1-3)
   - Enter database URL
   - Enter SQL query
   - Choose export format
   - Optionally send email

### Complete Example Session

```
$ python main.py

============================================================
Database Query, Export, and Email Tool
============================================================

============================================================
Select Database Type:
============================================================
1. Oracle
2. PostgreSQL
3. SQLite
============================================================
Enter your choice (1-3): 2

============================================================
Database URL found in .env file
============================================================
Database URL: postgresql://admin:mypassword@localhost:5432/company_db
============================================================
Use database URL from .env file? (yes/no, default: yes): yes
✓ Using database URL from .env file

============================================================
Enter SQL Query:
============================================================
(You can enter multi-line queries. Type 'END' on a new line to finish)
============================================================
SELECT 
    id,
    name,
    email,
    created_at
FROM users
WHERE created_at > '2024-01-01'
ORDER BY created_at DESC
END

============================================================
Export Options:
============================================================
1. Export to Excel (.xlsx) only
2. Export to PDF only
3. Export to both Excel and PDF
============================================================
Enter your choice (1-3): 1

Enter Excel output path (default: report.xlsx): users_report.xlsx

============================================================
Email Options:
============================================================
Do you want to send email? (yes/no): yes

============================================================
Email Subject:
============================================================
Enter email subject (default: Database Report): Monthly Users Report

============================================================
Email Recipients:
============================================================
Enter recipient email addresses separated by commas
Example: user1@example.com, user2@example.com, user3@example.com
(Press Enter to finish, or type 'DONE')
============================================================
Recipient emails (comma-separated): manager@company.com, hr@company.com, admin@company.com
  ✓ Added 3 recipients

✓ Total recipients: 3
  Recipients: manager@company.com, hr@company.com, admin@company.com

============================================================
CC Recipients (Optional):
============================================================
Enter CC recipient email addresses separated by commas
Example: cc1@example.com, cc2@example.com
(Press Enter to skip, or type 'DONE' to finish)
============================================================
CC emails (comma-separated, or press Enter to skip): archive@company.com
  ✓ Added CC: archive@company.com

✓ Total CC recipients: 1
  CC Recipients: archive@company.com

✓ Connected to PostgreSQL database
✓ Executing query...
✓ Query returned 150 rows
✓ Excel file created: users_report.xlsx
✓ Email sent successfully to: manager@company.com, hr@company.com, admin@company.com
  CC: archive@company.com
  Attachments: users_report.xlsx

✓ Process completed successfully!
```

---

## Usage Examples

### Example 1: Export to Excel Only (No Email)

**Use Case:** You just want to export query results to Excel file.

```
1. Select database: 3 (SQLite)
2. Database URL: sqlite:///data/sample.db
3. Query: SELECT * FROM products WHERE price > 100
4. Export option: 1 (Excel only)
5. Output path: products.xlsx
6. Send email: no
```

**Result:** Creates `products.xlsx` file in current directory.

---

### Example 2: Export to PDF and Send Email

**Use Case:** Generate PDF report and email it to team.

```
1. Select database: 1 (Oracle)
2. Database URL: oracle://scott:tiger@localhost:1521/XE
3. Query: SELECT * FROM employees WHERE department = 'Sales'
4. Export option: 2 (PDF only)
5. Output path: sales_team.pdf
6. Send email: yes
7. Subject: Sales Team Report - Q1 2024
8. Recipients: sales-manager@company.com, hr@company.com
```

**Result:** Creates `sales_team.pdf` and sends email with PDF attachment.

---

### Example 3: Export Both Formats and Email

**Use Case:** Export to both Excel and PDF, then email both files.

```
1. Select database: 2 (PostgreSQL)
2. Database URL: postgresql://user:pass@localhost:5432/mydb
3. Query: SELECT * FROM orders WHERE order_date = CURRENT_DATE
4. Export option: 3 (Both Excel and PDF)
5. Excel path: daily_orders.xlsx
6. PDF path: daily_orders.pdf
7. Send email: yes
8. Subject: Daily Orders Report
9. Recipients: operations@company.com
```

**Result:** Creates both files and sends email with both attachments.

---

### Example 4: Complex Multi-line Query

**Use Case:** Run a complex SQL query with joins and aggregations.

```
Enter SQL Query:
(You can enter multi-line queries. Type 'END' on a new line to finish)
SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(o.id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
    AND u.status = 'active'
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC
LIMIT 100
END
```

---

## Database URL Examples

### Oracle

```
oracle://username:password@host:port/service_name
```

**Examples:**
```
oracle://scott:tiger@localhost:1521/XE
oracle://hr:hr123@db.company.com:1521/ORCL
oracle://admin:secret@192.168.1.100:1521/PDB1
```

### PostgreSQL

```
postgresql://username:password@host:port/database
```

**Examples:**
```
postgresql://postgres:mypassword@localhost:5432/mydb
postgresql://admin:secret@db.company.com:5432/production
postgresql://user:pass@192.168.1.100:5432/test_db
```

### SQLite

```
sqlite:///path/to/database.db
```

**Examples:**
```
sqlite:///data/sample.db
sqlite:///home/user/databases/company.db
sqlite:///C:/Users/John/Documents/data.db  (Windows)
```

**Note:** Use forward slashes (`/`) even on Windows, or use absolute paths.

---

## Troubleshooting

### Email Issues

#### Problem: "Authentication failed" or "Invalid credentials"

**Solutions:**
1. **Gmail:**
   - Make sure you're using an **App Password**, not your regular Gmail password
   - Verify 2-Step Verification is enabled
   - Check that the app password doesn't have spaces
   - Regenerate the app password if needed

2. **Outlook:**
   - Make sure you're using an **App Password**, not your regular password
   - Verify Two-Factor Authentication is enabled
   - Check that the app password doesn't have dashes
   - Regenerate the app password if needed

#### Problem: "Connection refused" or "Cannot connect to SMTP server"

**Solutions:**
1. Check your internet connection
2. Verify SMTP host and port:
   - Gmail: `smtp.gmail.com:587`
   - Outlook: `smtp-mail.outlook.com:587`
3. Check firewall settings
4. Try port 465 with SSL (requires code modification)

#### Problem: "Less secure app access" error (Gmail)

**Solution:**
- This error means you're using your regular password
- You **must** use an App Password instead
- Follow the Gmail App Password setup steps above

### Database Connection Issues

#### Problem: "Failed to connect to PostgreSQL database"

**Solutions:**
1. Verify PostgreSQL server is running:
   ```bash
   # Check if PostgreSQL is running
   ps aux | grep postgres
   ```
2. Check database URL format
3. Verify username, password, and database name
4. Ensure `psycopg2-binary` is installed: `pip install psycopg2-binary`

#### Problem: "Failed to connect to Oracle database"

**Solutions:**
1. Verify Oracle client libraries are installed
2. Check service name/SID is correct
3. Verify host, port, and credentials
4. Test connection with Oracle SQL Developer first

#### Problem: "Failed to connect to SQLite database"

**Solutions:**
1. Verify file path is correct
2. Check file exists: `ls -la path/to/database.db`
3. Verify file permissions: `chmod 644 database.db`
4. Use absolute path if relative path doesn't work

### Export Issues

#### Problem: "Permission denied" when creating file

**Solutions:**
1. Check write permissions in output directory
2. Create output directory if it doesn't exist
3. Use absolute path for output file
4. Check disk space: `df -h`

#### Problem: "Module not found" errors

**Solutions:**
1. Make sure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python3 --version` (should be 3.8+)

### General Issues

#### Problem: Import errors when running

**Solution:**
Make sure you're running from the project root directory:
```bash
cd "/Users/aakash/Desktop/My workspace/oracle_db_connection"
python main.py
```

#### Problem: ".env file not found"

**Solution:**
1. Create `.env` file in project root (copy from `env.example`)
2. Add email configuration (only needed if sending emails)
3. Optionally add database URLs (or enter interactively)

---

## Quick Reference

### Gmail SMTP Settings
```
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

### Outlook SMTP Settings
```
SMTP_USER=your_email@outlook.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

### Database URL Configuration (.env)

You can optionally configure database URLs in `.env`:

```env
# Oracle
ORACLE_DATABASE_URL=oracle://username:password@host:1521/service_name

# PostgreSQL
POSTGRESQL_DATABASE_URL=postgresql://username:password@host:5432/database

# SQLite
SQLITE_DATABASE_URL=sqlite:///path/to/database.db
```

If set, the app will ask if you want to use the URL from `.env` or enter manually.

### Common Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Run application
python main.py

# Install dependencies
pip install -r requirements.txt

# Check Python version
python3 --version

# Copy .env example
cp env.example .env
```

---

## Need More Help?

1. Check error messages carefully - they usually indicate the issue
2. Verify all configuration in `.env` file
3. Test database connection separately
4. Test email sending with a simple script
5. Review the troubleshooting section above

---

**Last Updated:** 2024

