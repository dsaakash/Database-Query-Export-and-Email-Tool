# Database Connection and Excel Export Tool

Python tools to connect to databases (Oracle, PostgreSQL, SQLite), query tables, and export results to Excel/PDF files with email support.

## 🎯 New Interactive Tool (Recommended)

**`main.py`** - Interactive multi-database tool with clean architecture

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive tool
python main.py
```

### 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup and usage guide
- **[EMAIL_SETUP.md](EMAIL_SETUP.md)** - Gmail & Outlook email configuration

### Features

- ✅ **Multi-Database Support** - Oracle, PostgreSQL, SQLite
- ✅ **Interactive Prompts** - Step-by-step guided workflow
- ✅ **Excel & PDF Export** - Export query results to multiple formats
- ✅ **Email Functionality** - Send reports via Gmail or Outlook
- ✅ **Multiple Recipients** - Send to multiple email addresses
- ✅ **Clean Architecture** - SOLID principles, maintainable code

---

## 📧 Email Setup Guides

**Need to set up email?** Follow these guides:

- **[EMAIL_SETUP.md](EMAIL_SETUP.md)** - Step-by-step Gmail & Outlook setup
- **[SETUP_GUIDE.md](SETUP_GUIDE.md#email-setup)** - Complete email configuration guide

**Quick Links:**
- [Gmail App Password Setup](EMAIL_SETUP.md#-gmail-setup)
- [Outlook App Password Setup](EMAIL_SETUP.md#-outlook-setup)

---

## Available Tools

- **main.py** - ⭐ **NEW** Interactive multi-database tool (Oracle, PostgreSQL, SQLite)
- **main1.py** - Legacy Oracle 11g tool (command-line)

---

## SQLite Tool (main.py)

A single-file Python tool to connect to SQLite databases, query tables, and export results to Excel files.

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Create Sample Database (Optional)

If you don't have a SQLite database yet, create one with sample data:

```bash
python main.py init
```

This creates `data/sample.db` with a `sample_table` containing 5 sample records.

**Custom database:**
```bash
python main.py init --db-path data/my_database.db --table-name my_table
```

### Step 3: Configure Database Connection

Edit the `.env` file in the project root:

```env
database_url=sqlite:///data/sample.db
port=
```

**Supported SQLite URL formats:**
- `sqlite:///data/sample.db` (recommended)
- `sqlite:data/sample.db`
- `data/sample.db` (direct file path)

### Step 4: Run the Export

Query a table and export to Excel:

```bash
python main.py export --table sample_table --output report.xlsx
```

**That's it!** The Excel file will be created in the project root.

---

## 📖 How to Run

### Command Structure

```bash
python main.py <command> [options]
```

### Available Commands

#### 1. Initialize Database (`init`)

Create a new SQLite database with a sample table:

```bash
python main.py init [--db-path PATH] [--table-name NAME]
```

**Options:**
- `--db-path`: Path to SQLite database file (default: `data/sample.db`)
- `--table-name`: Name of the sample table (default: `sample_table`)

**Examples:**
```bash
# Use defaults
python main.py init

# Custom path and table name
python main.py init --db-path data/my_db.db --table-name employees
```

#### 2. Export Table (`export`)

Query a database table and export to Excel:

```bash
python main.py export --table TABLE_NAME [--output PATH] [--env-file PATH]
```

**Options:**
- `--table`: Name of the table to query (required)
- `--output`: Output Excel file path (default: `report.xlsx`)
- `--env-file`: Custom `.env` file path (default: `.env` in project root)

**Examples:**
```bash
# Basic export
python main.py export --table sample_table

# Custom output location
python main.py export --table sample_table --output exports/my_report.xlsx

# Use custom .env file
python main.py export --table sample_table --env-file .env.production
```

---

## 📋 Complete Workflow Example

Here's a complete example from start to finish:

```bash
# 1. Navigate to project directory
cd oracle_db_connection

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create sample database
python main.py init

# 5. Verify .env file has correct database URL
cat .env
# Should show: database_url=sqlite:///data/sample.db

# 6. Export table to Excel
python main.py export --table sample_table --output report.xlsx

# 7. Check the output
ls -lh report.xlsx
```

**Expected output:**
```
✓ Successfully exported to: /path/to/oracle_db_connection/report.xlsx
```

---

## 🔧 Configuration

### Environment Variables (.env file)

Create or edit `.env` in the project root:

```env
# Database connection URL
# For SQLite, use one of these formats:
database_url=sqlite:///data/sample.db
# OR
database_url=sqlite:data/sample.db
# OR
database_url=data/sample.db

# Port (not used for SQLite, can be left empty)
port=
```

### Database URL Formats

The tool automatically detects SQLite databases from these URL patterns:

| Format | Example | Description |
|--------|---------|-------------|
| `sqlite:///path` | `sqlite:///data/db.db` | Standard SQLite URL |
| `sqlite:path` | `sqlite:data/db.db` | Alternative format |
| Direct path | `data/db.db` | File path without scheme |

---

## 📁 Project Structure

```
oracle_db_connection/
├── main.py              # Single-file application (all code here!)
├── .env                 # Configuration file
├── requirements.txt     # Python dependencies
├── data/                # SQLite database files (created automatically)
├── README.md            # This file
└── .gitignore          # Git ignore rules
```

**Note:** This is a single-file application. All functionality is in `main.py`.

---

## ✅ What It Does

1. **Connects** to your SQLite database using the URL from `.env`
2. **Queries** the specified table with `SELECT * FROM table_name`
3. **Exports** all records to an Excel file (`.xlsx` format)
4. **Handles** errors gracefully with clear error messages

---

## 🐛 Troubleshooting

### Error: "database_url not found in environment"
**Solution:** Make sure `.env` file exists in the project root and contains `database_url=...`

### Error: "unable to open database file"
**Solution:** 
- Check that the database file path in `.env` is correct
- Ensure the database file exists
- Use absolute path if relative path doesn't work

### Error: "Table 'X' is empty or does not exist"
**Solution:**
- Verify the table name is spelled correctly
- Check that the table exists in your database
- Use SQLite browser to inspect your database: `sqlite3 data/sample.db "SELECT name FROM sqlite_master WHERE type='table';"`

### Error: "Cannot export empty query result"
**Solution:** The table exists but has no data. Add some records to the table first.

### Import Errors
**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Command Not Found
**Solution:** Make sure you're using the correct command syntax:
```bash
# Correct
python main.py export --table sample_table

# Wrong
python main.py --table sample_table  # Missing 'export' command
```

---

## 📦 Requirements

- Python 3.8+
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- python-dotenv >= 1.0.0

---

## 💡 Tips

1. **Use virtual environments** to avoid dependency conflicts
2. **Check your database** first with a SQLite browser tool
3. **Use absolute paths** in `.env` if relative paths cause issues
4. **Organize exports** by creating subdirectories: `exports/reports/`
5. **Single file** - All code is in `main.py`, easy to understand and modify

---

## 🔍 Verify Your Setup

Test that everything works:

```bash
# 1. Check Python version
python3 --version  # Should be 3.8+

# 2. Check dependencies
pip list | grep -E "(pandas|openpyxl|python-dotenv)"

# 3. Test database initialization
python main.py init --db-path data/test.db

# 4. Test export
python main.py export --table sample_table --output test.xlsx

# 5. Verify Excel file
python3 -c "import pandas as pd; df = pd.read_excel('test.xlsx'); print(f'✓ {len(df)} rows exported')"
```

---

## 📝 Usage Examples

### Example 1: Quick Start with Defaults
```bash
# Initialize database
python main.py init

# Export to Excel
python main.py export --table sample_table
```

### Example 2: Custom Database and Table
```bash
# Create custom database
python main.py init --db-path data/company.db --table-name employees

# Update .env
echo "database_url=sqlite:///data/company.db" > .env

# Export
python main.py export --table employees --output employees.xlsx
```

### Example 3: Multiple Tables
```bash
# Export different tables to different files
python main.py export --table products --output products.xlsx
python main.py export --table orders --output orders.xlsx
python main.py export --table customers --output customers.xlsx
```

### Example 4: Organized Output
```bash
# Create exports directory
mkdir -p exports

# Export to organized location
python main.py export --table sample_table --output exports/2025-12-05_report.xlsx
```

---

## 🎯 Key Features

- ✅ **Single-file application** - Everything in `main.py`
- ✅ **Simple commands** - `init` and `export` subcommands
- ✅ **Automatic SQLite detection** - Works with various URL formats
- ✅ **Excel export** - Clean, formatted Excel files
- ✅ **Error handling** - Clear error messages
- ✅ **Environment configuration** - Easy `.env` setup

## 🆘 Need Help?

1. Check the `.env` file configuration
2. Verify the database file exists
3. Ensure the table name is correct
4. Check error messages for specific issues
5. Review the command help: `python main.py --help`

For more details, see the code comments in `main.py`.

---

## Oracle 11g Tool (main1.py)

A single-file Python tool for Oracle 11g databases with Excel/PDF export and email functionality.

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure .env file:**
   ```env
   ORACLE_HOST=localhost
   ORACLE_PORT=1521
   ORACLE_SERVICE_NAME=XE
   ORACLE_USERNAME=hr
   ORACLE_PASSWORD=your_password
   
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   RECEIVER_EMAIL=recipient@example.com
   ```

3. **Run query and export:**
   ```bash
   python main1.py --query "SELECT COURSE_NAME, COURSE_ID, FEES FROM DUMMY_COURSES" --excel report.xlsx
   ```

### Features

- ✅ Connect to Oracle 11g database
- ✅ Execute SQL queries
- ✅ Export to Excel (`.xlsx`)
- ✅ Export to PDF (`.pdf`)
- ✅ Convert to HTML table
- ✅ Send email with HTML body and attachments
- ✅ Environment-based configuration

### Documentation

- **Quick Start**: See `QUICK_START_ORACLE.md`
- **Complete Guide**: See `ORACLE_SETUP_GUIDE.md` (includes database setup, table creation, and step-by-step instructions)



oracle_db_connection/
├── main.py              # Single-file application (all code here!)
├── .env                 # Configuration
├── requirements.txt     # Dependencies
├── data/                # Database files
└── README.md            # Updated documentation