# Oracle 11g Database Setup and Usage Guide

Complete step-by-step guide for setting up Oracle 11g database, creating tables, and using `main1.py` to export data to Excel/PDF and send emails.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Oracle Database Setup](#oracle-database-setup)
4. [Create Database and Tables](#create-database-and-tables)
5. [Configuration (.env Setup)](#configuration-env-setup)
6. [Using main1.py](#using-main1py)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.8 or higher
- Oracle 11g Database installed and running
- Oracle Instant Client (for oracledb)
- Access to Oracle database with CREATE TABLE privileges
- Email account for sending reports (Gmail, Outlook, etc.)

---

## Installation

### Step 1: Install Python Dependencies

```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

This installs:
- `oracledb` - Oracle database driver
- `pandas` - Data manipulation
- `openpyxl` - Excel file support
- `yagmail` - Email sending
- `reportlab` - PDF generation
- `python-dotenv` - Environment configuration

### Step 2: Install Oracle Instant Client

The `oracledb` package requires Oracle Instant Client.

#### For macOS:
```bash
# Using Homebrew
brew install instantclient-basic

# Or download from Oracle website:
# https://www.oracle.com/database/technologies/instant-client/downloads.html
```

#### For Linux:
```bash
# Download Oracle Instant Client Basic Package
# https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

# Extract and set environment variables
export LD_LIBRARY_PATH=/path/to/instantclient_21_1:$LD_LIBRARY_PATH
```

#### For Windows:
1. Download Oracle Instant Client from Oracle website
2. Extract to a folder (e.g., `C:\oracle\instantclient_21_1`)
3. Add to PATH environment variable

---

## Oracle Database Setup

### Step 1: Verify Oracle Database is Running

```bash
# Check if Oracle service is running
# On Linux/Unix:
ps aux | grep pmon

# On Windows:
# Check Services for OracleService<ORACLE_SID>
```

### Step 2: Connect to Oracle Database

```bash
# Using SQL*Plus
sqlplus username/password@hostname:port/service_name

# Example:
sqlplus hr/hr@localhost:1521/XE
```

### Step 3: Verify Connection

```sql
-- Test connection
SELECT * FROM DUAL;
```

---

## Create Database and Tables

### Step 1: Connect as Administrator

```bash
sqlplus sys/password@localhost:1521/XE AS SYSDBA
```

Or connect as a user with CREATE TABLE privileges:

```bash
sqlplus hr/hr@localhost:1521/XE
```

### Step 2: Create Tablespace (Optional)

If you need a custom tablespace:

```sql
-- Create tablespace
CREATE TABLESPACE my_tablespace
DATAFILE 'C:\oracle\oradata\XE\my_tablespace.dbf' SIZE 100M
AUTOEXTEND ON NEXT 10M MAXSIZE 500M;

-- Create user (optional)
CREATE USER my_user IDENTIFIED BY my_password
DEFAULT TABLESPACE my_tablespace
TEMPORARY TABLESPACE temp;

-- Grant privileges
GRANT CONNECT, RESOURCE, CREATE TABLE TO my_user;
```

### Step 3: Create Sample Table

```sql
-- Create DUMMY_COURSES table
CREATE TABLE DUMMY_COURSES (
    COURSE_ID NUMBER PRIMARY KEY,
    COURSE_NAME VARCHAR2(100) NOT NULL,
    FEES NUMBER(10, 2),
    DURATION_DAYS NUMBER,
    INSTRUCTOR VARCHAR2(100),
    CREATED_DATE DATE DEFAULT SYSDATE
);

-- Create sequence for auto-increment
CREATE SEQUENCE course_seq
START WITH 1
INCREMENT BY 1
NOCACHE;

-- Create trigger for auto-increment
CREATE OR REPLACE TRIGGER course_trigger
BEFORE INSERT ON DUMMY_COURSES
FOR EACH ROW
BEGIN
    IF :NEW.COURSE_ID IS NULL THEN
        :NEW.COURSE_ID := course_seq.NEXTVAL;
    END IF;
END;
/
```

### Step 4: Insert Sample Data

```sql
-- Insert sample data
INSERT INTO DUMMY_COURSES (COURSE_NAME, FEES, DURATION_DAYS, INSTRUCTOR) VALUES
('Python Programming', 5000.00, 30, 'John Smith');
INSERT INTO DUMMY_COURSES (COURSE_NAME, FEES, DURATION_DAYS, INSTRUCTOR) VALUES
('Java Development', 6000.00, 45, 'Jane Doe');
INSERT INTO DUMMY_COURSES (COURSE_NAME, FEES, DURATION_DAYS, INSTRUCTOR) VALUES
('Database Administration', 7000.00, 60, 'Bob Johnson');
INSERT INTO DUMMY_COURSES (COURSE_NAME, FEES, DURATION_DAYS, INSTRUCTOR) VALUES
('Web Development', 5500.00, 40, 'Alice Williams');
INSERT INTO DUMMY_COURSES (COURSE_NAME, FEES, DURATION_DAYS, INSTRUCTOR) VALUES
('Data Science', 8000.00, 90, 'Charlie Brown');

-- Commit changes
COMMIT;

-- Verify data
SELECT * FROM DUMMY_COURSES;
```

### Step 5: Grant Permissions (if needed)

```sql
-- Grant SELECT permission to user
GRANT SELECT ON DUMMY_COURSES TO your_username;

-- Or if you own the table, no grant needed
```

---

## Configuration (.env Setup)

### Step 1: Create .env File

Create a `.env` file in the project root:

```bash
touch .env
```

### Step 2: Add Oracle Configuration

Add the following to `.env`:

```env
# Oracle Database Configuration
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XE
ORACLE_USERNAME=hr
ORACLE_PASSWORD=your_password

# Alternative: Use SID instead of SERVICE_NAME
# ORACLE_SID=XE

# Email Configuration (for sending reports)
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
RECEIVER_EMAIL=recipient@example.com
```

### Step 3: Gmail App Password Setup

If using Gmail, you need to create an App Password:

1. Go to Google Account settings
2. Security → 2-Step Verification (enable if not enabled)
3. App passwords → Generate app password
4. Use the generated password in `SMTP_PASSWORD`

### Step 4: Other Email Providers

**Outlook/Hotmail:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo:**
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Custom SMTP:**
```env
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587
```

---

## Using main1.py

### Basic Usage

```bash
python main1.py --query "YOUR_SQL_QUERY" [OPTIONS]
```

### Command Options

- `--query`: SQL query to execute (required)
- `--excel`: Output Excel file path (default: `test_report.xlsx`)
- `--pdf`: Output PDF file path (optional)
- `--send-email`: Send email with report
- `--subject`: Email subject (default: "Test Report")
- `--env-file`: Custom .env file path

### Example 1: Basic Query and Excel Export

```bash
python main1.py --query "SELECT COURSE_NAME, COURSE_ID, FEES FROM DUMMY_COURSES" --excel courses_report.xlsx
```

### Example 2: Export to Excel and PDF

```bash
python main1.py \
  --query "SELECT COURSE_NAME, COURSE_ID, FEES FROM DUMMY_COURSES" \
  --excel courses.xlsx \
  --pdf courses.pdf
```

### Example 3: Query, Export, and Send Email

```bash
python main1.py \
  --query "SELECT COURSE_NAME, COURSE_ID, FEES FROM DUMMY_COURSES" \
  --excel courses.xlsx \
  --pdf courses.pdf \
  --send-email \
  --subject "Daily Courses Report"
```

### Example 4: Complex Query

```bash
python main1.py \
  --query "SELECT COURSE_NAME, COURSE_ID, FEES, DURATION_DAYS, INSTRUCTOR FROM DUMMY_COURSES WHERE FEES > 6000 ORDER BY FEES DESC" \
  --excel expensive_courses.xlsx \
  --send-email \
  --subject "High-Value Courses Report"
```

---

## Examples

### Example 1: Complete Workflow

```bash
# 1. Create table in Oracle (using SQL*Plus)
sqlplus hr/hr@localhost:1521/XE

# In SQL*Plus:
CREATE TABLE DUMMY_COURSES (
    COURSE_ID NUMBER PRIMARY KEY,
    COURSE_NAME VARCHAR2(100),
    FEES NUMBER(10, 2)
);

INSERT INTO DUMMY_COURSES VALUES (1, 'Python', 5000);
INSERT INTO DUMMY_COURSES VALUES (2, 'Java', 6000);
COMMIT;
EXIT;

# 2. Configure .env file with Oracle and email settings

# 3. Run query and export
python main1.py \
  --query "SELECT COURSE_NAME, COURSE_ID, FEES FROM DUMMY_COURSES" \
  --excel report.xlsx \
  --send-email
```

### Example 2: Scheduled Reports

Create a cron job (Linux/macOS) or scheduled task (Windows) to run reports automatically:

```bash
# Add to crontab (runs daily at 9 AM)
0 9 * * * cd /path/to/oracle_db_connection && /path/to/python main1.py --query "SELECT * FROM DUMMY_COURSES" --excel daily_report.xlsx --send-email --subject "Daily Report"
```

---

## Troubleshooting

### Error: "ORA-12154: TNS:could not resolve the connect identifier"

**Solution:**
- Check `ORACLE_HOST`, `ORACLE_PORT`, and `ORACLE_SERVICE_NAME` in `.env`
- Verify Oracle database is running
- Test connection with SQL*Plus first

### Error: "ORA-01017: invalid username/password"

**Solution:**
- Verify `ORACLE_USERNAME` and `ORACLE_PASSWORD` in `.env`
- Check if account is locked: `ALTER USER username ACCOUNT UNLOCK;`

### Error: "ORA-00942: table or view does not exist"

**Solution:**
- Verify table name is correct (case-sensitive in Oracle)
- Check if you have SELECT permission on the table
- Use schema prefix: `SELECT * FROM SCHEMA_NAME.TABLE_NAME`

### Error: "ModuleNotFoundError: No module named 'oracledb'"

**Solution:**
```bash
pip install oracledb
```

### Error: "Oracle Client library not found"

**Solution:**
- Install Oracle Instant Client
- Set `LD_LIBRARY_PATH` (Linux/macOS) or add to PATH (Windows)
- For macOS with Homebrew: `brew install instantclient-basic`

### Error: "SMTP Authentication failed"

**Solution:**
- For Gmail: Use App Password, not regular password
- Enable "Less secure app access" (if available) or use App Password
- Check SMTP credentials in `.env`

### Error: "Email sending failed"

**Solution:**
- Verify SMTP settings (host, port)
- Check firewall settings
- Test SMTP connection separately
- For Gmail: Ensure 2-Step Verification is enabled and use App Password

### Query Returns No Results

**Solution:**
- Verify table has data: `SELECT COUNT(*) FROM TABLE_NAME;`
- Check WHERE clause conditions
- Verify table name and column names are correct

---

## Additional SQL Examples

### Create More Tables

```sql
-- Create EMPLOYEES table
CREATE TABLE EMPLOYEES (
    EMP_ID NUMBER PRIMARY KEY,
    EMP_NAME VARCHAR2(100),
    DEPARTMENT VARCHAR2(50),
    SALARY NUMBER(10, 2),
    HIRE_DATE DATE
);

-- Create ORDERS table
CREATE TABLE ORDERS (
    ORDER_ID NUMBER PRIMARY KEY,
    CUSTOMER_NAME VARCHAR2(100),
    ORDER_DATE DATE,
    AMOUNT NUMBER(10, 2),
    STATUS VARCHAR2(20)
);
```

### Useful Queries

```sql
-- Get all tables
SELECT table_name FROM user_tables;

-- Get table structure
DESC DUMMY_COURSES;

-- Count records
SELECT COUNT(*) FROM DUMMY_COURSES;

-- Get table size
SELECT segment_name, bytes/1024/1024 AS size_mb
FROM user_segments
WHERE segment_type = 'TABLE';
```

---

## Best Practices

1. **Use Parameterized Queries**: For production, use parameterized queries to prevent SQL injection
2. **Connection Pooling**: For high-volume applications, use connection pooling
3. **Error Handling**: Always handle database errors gracefully
4. **Logging**: Add logging for debugging and monitoring
5. **Security**: Never commit `.env` file with real credentials to version control
6. **Backup**: Regularly backup your database
7. **Indexing**: Add indexes on frequently queried columns

---

## Next Steps

- Customize email templates
- Add more export formats (CSV, JSON)
- Implement scheduled reports
- Add data validation
- Create dashboard views

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all configuration in `.env`
3. Test Oracle connection separately
4. Review error messages carefully

---

**Happy Querying! 🚀**

