# Database Query, Export, and Email Tool

An interactive Python application for connecting to multiple database types (Oracle, PostgreSQL, SQLite), querying tables, exporting to Excel/PDF, and sending email reports.

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Email (Optional - only if sending emails)

Create a `.env` file in the project root:

```env
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**Gmail App Password Setup:**
1. Go to [Google Account Settings](https://myaccount.google.com/) > Security
2. Enable 2-Step Verification (if not already enabled)
3. Go to "App Passwords" and generate a new app password
4. Use that app password in `.env` (not your regular Gmail password)

### Step 3: Run the Application

```bash
python main.py
```

The application will guide you through:
1. **Database Selection** - Choose Oracle, PostgreSQL, or SQLite
2. **Database URL** - Enter connection string
3. **SQL Query** - Enter your query (supports multi-line)
4. **Export Options** - Choose Excel, PDF, or both
5. **Email Options** - Optionally send email with attachments

## 📖 Usage Guide

### Interactive Flow

When you run `python main.py`, you'll be prompted step-by-step:

```
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
Enter POSTGRESQL Database URL:
============================================================
Format: postgresql://username:password@host:port/database
Example: postgresql://user:pass@localhost:5432/mydb
============================================================
Database URL: postgresql://user:pass@localhost:5432/mydb

============================================================
Enter SQL Query:
============================================================
(You can enter multi-line queries. Type 'END' on a new line to finish)
============================================================
SELECT * FROM users
WHERE created_at > '2024-01-01'
END

============================================================
Export Options:
============================================================
1. Export to Excel (.xlsx) only
2. Export to PDF only
3. Export to both Excel and PDF
============================================================
Enter your choice (1-3): 1

Enter Excel output path (default: report.xlsx): my_report.xlsx

============================================================
Email Options:
============================================================
Do you want to send email? (yes/no): yes

============================================================
Email Subject:
============================================================
Enter email subject (default: Database Report): Monthly User Report

============================================================
Email Recipients:
============================================================
Enter recipient email addresses separated by commas
Example: user1@example.com, user2@example.com, user3@example.com
(Press Enter to finish, or type 'DONE')
============================================================
Recipient emails (comma-separated): user1@example.com, user2@example.com, user3@example.com
  ✓ Added 3 recipients

✓ Total recipients: 3
  Recipients: user1@example.com, user2@example.com, user3@example.com

============================================================
CC Recipients (Optional):
============================================================
Enter CC recipient email addresses separated by commas
Example: cc1@example.com, cc2@example.com
(Press Enter to skip, or type 'DONE' to finish)
============================================================
CC emails (comma-separated, or press Enter to skip): archive@example.com
  ✓ Added CC: archive@example.com

✓ Total CC recipients: 1
  CC Recipients: archive@example.com

✓ Connected to PostgreSQL database
✓ Executing query...
✓ Query returned 150 rows
✓ Excel file created: my_report.xlsx
✓ Email sent successfully to: user1@example.com, user2@example.com, user3@example.com
  CC: archive@example.com
  Attachments: my_report.xlsx

✓ Process completed successfully!
```

## 🗄️ Database URL Formats

### Oracle
```
oracle://username:password@host:port/service_name
```
**Example:**
```
oracle://scott:tiger@localhost:1521/XE
```

### PostgreSQL
```
postgresql://username:password@host:port/database
```
**Example:**
```
postgresql://user:pass@localhost:5432/mydb
```

### SQLite
```
sqlite:///path/to/database.db
```
**Example:**
```
sqlite:///data/sample.db
```

## 📋 Features

### ✅ Multi-Database Support
- **Oracle** - Full Oracle 11g+ support
- **PostgreSQL** - Standard PostgreSQL connections
- **SQLite** - Local SQLite database files

### ✅ Export Formats
- **Excel (.xlsx)** - Clean, formatted spreadsheets
- **PDF (.pdf)** - Professional PDF reports with styling

### ✅ Email Functionality
- **Multiple Recipients** - Send to multiple email addresses (TO)
- **CC Support** - Carbon copy recipients (optional)
- **HTML Body** - Formatted HTML table in email body
- **Attachments** - Excel and/or PDF files attached
- **Gmail Integration** - Uses Gmail SMTP with app passwords

### ✅ Interactive Interface
- **Step-by-step prompts** - Guided workflow
- **Multi-line queries** - Support for complex SQL
- **Flexible options** - Choose export formats and email settings

## 🏗️ Architecture

The application follows **Clean Architecture** and **SOLID principles**:

```
src/
├── core/                    # Core domain interfaces
│   ├── interfaces.py       # Database adapter interface
│   ├── config.py          # Configuration management
│   └── prompts.py         # Interactive prompt service
├── adapters/              # External service adapters
│   └── database/         # Database adapters
│       ├── oracle_adapter.py
│       ├── postgresql_adapter.py
│       ├── sqlite_adapter.py
│       └── factory.py    # Factory pattern for adapters
└── services/             # Business logic services
    ├── export_service.py # Excel/PDF export services
    ├── email_service.py  # Email sending service
    └── query_service.py  # Query orchestration service
```

### Design Patterns Used

- **Factory Pattern** - `DatabaseAdapterFactory` creates appropriate adapters
- **Adapter Pattern** - Database adapters implement unified interface
- **Dependency Inversion** - Depend on abstractions, not concretions
- **Single Responsibility** - Each class has one clear purpose
- **Open/Closed** - Easy to add new database types without modifying existing code

## 📦 Requirements

- Python 3.8+
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- python-dotenv >= 1.0.0
- oracledb >= 2.0.0
- yagmail >= 0.15.0
- reportlab >= 4.0.0
- psycopg2-binary >= 2.9.0
- sqlalchemy >= 2.0.0

## 🔧 Configuration

### Environment Variables (.env)

Create `.env` file in project root (copy from `env.example`):

```bash
cp env.example .env
```

Edit `.env` with your configuration:

```env
# Email Configuration (required only if sending emails)
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

# Database URLs (optional - can also enter interactively)
ORACLE_DATABASE_URL=oracle://user:pass@host:1521/service_name
POSTGRESQL_DATABASE_URL=postgresql://user:pass@host:5432/database
SQLITE_DATABASE_URL=sqlite:///path/to/database.db
```

**Note:** 
- Database URLs are **optional** - you can enter them interactively or configure in `.env`
- If database URL is set in `.env`, the app will ask if you want to use it
- Email configuration is required only if you plan to send emails

## 💡 Usage Examples

### Example 1: Export to Excel Only

```
1. Select database: PostgreSQL
2. Enter URL: postgresql://user:pass@localhost:5432/mydb
3. Enter query: SELECT * FROM products WHERE price > 100
4. Export option: Excel only
5. Output path: products.xlsx
6. Send email: No
```

### Example 2: Export to PDF and Send Email

```
1. Select database: Oracle
2. Enter URL: oracle://scott:tiger@localhost:1521/XE
3. Enter query: SELECT * FROM employees WHERE department = 'Sales'
4. Export option: PDF only
5. Output path: sales_report.pdf
6. Send email: Yes
7. Subject: Sales Team Report
8. Recipients: manager@company.com, hr@company.com
```

### Example 3: Multi-line Query

```
Enter SQL Query:
(You can enter multi-line queries. Type 'END' on a new line to finish)
SELECT 
    u.id,
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC
END
```

## 🐛 Troubleshooting

### Database Connection Errors

**Oracle:**
- Verify Oracle client libraries are installed
- Check service name/SID is correct
- Ensure firewall allows connection

**PostgreSQL:**
- Verify PostgreSQL server is running
- Check database name and credentials
- Ensure `psycopg2-binary` is installed

**SQLite:**
- Verify file path is correct
- Ensure file exists and is readable
- Use absolute path if relative path fails

### Email Sending Errors

**"Authentication failed":**
- Use Gmail App Password, not regular password
- Enable 2-Step Verification in Google Account
- Verify SMTP credentials in `.env`

**"Connection refused":**
- Check SMTP host and port
- Verify firewall allows SMTP connections
- Try different SMTP port (465 for SSL)

### Export Errors

**"Permission denied":**
- Check write permissions for output directory
- Ensure output path is valid
- Create output directory if it doesn't exist

## 🎯 Key Features

- ✅ **Clean Architecture** - Separation of concerns
- ✅ **SOLID Principles** - Maintainable, extensible code
- ✅ **Multi-Database** - Oracle, PostgreSQL, SQLite support
- ✅ **Interactive Prompts** - User-friendly interface
- ✅ **Multiple Recipients** - Send emails to multiple addresses (TO and CC)
- ✅ **Flexible Exports** - Excel, PDF, or both
- ✅ **Error Handling** - Clear error messages
- ✅ **Type Hints** - Better code documentation

## 📝 Project Structure

```
oracle_db_connection/
├── main.py                 # Main entry point
├── src/                    # Source code
│   ├── core/              # Core interfaces and config
│   ├── adapters/         # Database adapters
│   └── services/         # Business logic services
├── .env                   # Configuration (create from .env.example)
├── .env.example          # Example configuration
├── requirements.txt      # Python dependencies
└── README_NEW.md        # This file
```

## 🆘 Need Help?

1. Check `.env` file configuration (for email)
2. Verify database URL format matches examples
3. Ensure all dependencies are installed
4. Check error messages for specific issues
5. Review database connection requirements

---

**Note:** This is the new interactive version. The old `main1.py` is still available for command-line usage.

