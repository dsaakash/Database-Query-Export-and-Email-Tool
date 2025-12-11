# Quick Start Guide

Get up and running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure .env File

Create `.env` file from example:

```bash
cp env.example .env
```

Edit `.env` with your settings:

**Email (Required only if sending emails):**
```env
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**Database URLs (Optional - can also enter interactively):**
```env
# Oracle
ORACLE_DATABASE_URL=oracle://user:pass@host:1521/service_name

# PostgreSQL
POSTGRESQL_DATABASE_URL=postgresql://user:pass@host:5432/database

# SQLite
SQLITE_DATABASE_URL=sqlite:///path/to/database.db
```

**Note:** If database URL is set in `.env`, the app will ask if you want to use it.

**How to get App Password:**
- **Gmail:** [Google Account > Security > App Passwords](https://myaccount.google.com/apppasswords)
- **Outlook:** [Microsoft Account > Security > App Passwords](https://account.microsoft.com/security)

### 3. Run the Application

```bash
python main.py
```

## 📝 Example Usage

```
1. Select database: 2 (PostgreSQL)
2. Database URL: postgresql://user:pass@localhost:5432/mydb
3. Query: SELECT * FROM users LIMIT 10
   (Type 'END' to finish)
4. Export: 1 (Excel only)
5. Output: report.xlsx
6. Email: no
```

## 🎯 Common Use Cases

### Export to Excel Only
```
Database: Your choice
URL: Your database URL
Query: Your SQL query
Export: Option 1 (Excel only)
Email: no
```

### Export and Email
```
Database: Your choice
URL: Your database URL
Query: Your SQL query
Export: Option 1 or 3
Email: yes
Recipients: email1@example.com, email2@example.com, email3@example.com
(Enter all recipients in one line, separated by commas)
CC Recipients: cc1@example.com, cc2@example.com (optional, press Enter to skip)
```

## 📚 Full Documentation

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## ⚡ Quick Troubleshooting

**Email not working?**
- Use App Password, not regular password
- Enable 2-Step Verification first

**Database connection failed?**
- Check URL format matches examples
- Verify credentials are correct

**Import errors?**
- Activate virtual environment
- Run: `pip install -r requirements.txt`

---

**That's it! You're ready to go! 🎉**

