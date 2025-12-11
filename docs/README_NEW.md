# Database Query, Export, and Email Tool

An interactive Python application for connecting to PostgreSQL databases, querying tables, exporting to Excel/PDF, and sending email reports.

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Run the Application

**Note:** Email configuration is now prompted interactively when you choose to send emails. You no longer need to configure it in `.env` file.

```bash
python main.py
```

The application will guide you through:
1. **Database URL** - Enter PostgreSQL connection string
2. **Connection Test** - Verify connection and list available tables
3. **SQL Query** - Enter your query (supports multi-line) or select from tables
4. **Export Options** - Choose Excel, PDF, or both
5. **Email Options** - Optionally send email with attachments (prompts for email config)

## 📖 Usage Guide

### Interactive Flow

When you run `python main.py`, you'll be prompted step-by-step:

```
============================================================
PostgreSQL Query, Export, and Email Tool
============================================================

============================================================
Database Type: PostgreSQL
============================================================
This application supports PostgreSQL database connections.
============================================================

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

## 🗄️ PostgreSQL Database URL Format

```
postgresql://username:password@host:port/database
```

**Examples:**
```
postgresql://user:pass@localhost:5432/mydb
postgresql://postgres:mypassword@db.example.com:5432/production
postgres://admin:secret@192.168.1.100:5432/test_db
```

**Alternative format:**
```
postgres://username:password@host:port/database
```

Both `postgresql://` and `postgres://` prefixes are supported.

## 📋 Features

### ✅ PostgreSQL Support
- **PostgreSQL** - Full PostgreSQL database support
- **Connection Status** - Real-time connection status display
- **Table Discovery** - Automatic table listing
- **Sample Tables** - Create sample tables with dummy data

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
# PostgreSQL Database URL (optional - can also enter interactively)
POSTGRESQL_DATABASE_URL=postgresql://user:pass@host:5432/database
```

**Note:** 
- Database URL is **optional** - you can enter it interactively or configure in `.env`
- If database URL is set in `.env`, the app will ask if you want to use it
- **Email configuration is now prompted interactively** - no need to configure in `.env`

## 💡 Usage Examples

### Example 1: Export to Excel Only

```
1. Enter URL: postgresql://user:pass@localhost:5432/mydb
2. Enter query: SELECT * FROM products WHERE price > 100
3. Export option: Excel only
4. Output path: products.xlsx
5. Send email: No
```

### Example 2: Export to PDF and Send Email

```
1. Enter URL: postgresql://user:pass@localhost:5432/mydb
2. Enter query: SELECT * FROM employees WHERE department = 'Sales'
3. Export option: PDF only
4. Output path: sales_report.pdf
5. Send email: Yes
6. Email config: (prompted interactively)
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

**PostgreSQL:**
- Verify PostgreSQL server is running
- Check database name and credentials
- Ensure `psycopg2-binary` is installed
- For cloud databases (Neon, Supabase, etc.):
  - Verify the connection string is correct
  - Check if your IP is whitelisted
  - Ensure the database instance is active
  - Check DNS resolution if hostname cannot be resolved

### Email Sending Errors

**"Authentication failed":**
- Use Gmail App Password, not regular password
- Enable 2-Step Verification in Google Account
- Verify SMTP credentials entered during prompt

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
- ✅ **PostgreSQL Support** - Full PostgreSQL database support
- ✅ **Interactive Prompts** - User-friendly interface
- ✅ **Multiple Recipients** - Send emails to multiple addresses (TO and CC)
- ✅ **Flexible Exports** - Excel, PDF, or both
- ✅ **Error Handling** - Clear error messages
- ✅ **Type Hints** - Better code documentation
- ✅ **Table Discovery** - Automatic table listing
- ✅ **Connection Status** - Real-time connection feedback

## 📝 Project Structure

```
oracle_db_connection/
├── main.py                 # Main entry point
├── src/                    # Source code
│   ├── core/              # Core interfaces and config
│   ├── adapters/         # Database adapters (PostgreSQL)
│   └── services/         # Business logic services
├── docs/                  # Documentation
│   ├── QUICK_START.md
│   ├── SETUP_GUIDE.md
│   ├── EMAIL_SETUP.md
│   └── GUIDES_INDEX.md
├── env.example           # Example configuration
├── requirements.txt      # Python dependencies
└── README.md            # Main README
```

## 🆘 Need Help?

1. Check database URL format matches examples
2. Ensure all dependencies are installed
3. Check error messages for specific issues
4. Review database connection requirements
5. See [docs/QUICK_START.md](QUICK_START.md) for quick setup
6. See [docs/SETUP_GUIDE.md](SETUP_GUIDE.md) for complete guide
7. See [docs/EMAIL_SETUP.md](EMAIL_SETUP.md) for email configuration

---

**Note:** This is the new interactive version. The old `main1.py` is still available for command-line usage.

