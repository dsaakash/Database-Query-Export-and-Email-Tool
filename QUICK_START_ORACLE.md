# Quick Start Guide - Oracle 11g (main1.py)

Quick reference for using `main1.py` with Oracle 11g database.

---

## 🚀 Quick Setup (5 Minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure .env File

Create `.env` file with Oracle and email settings:

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

### 3. Create Sample Table in Oracle

```sql
-- Connect to Oracle
sqlplus hr/hr@localhost:1521/XE

-- Create table
CREATE TABLE DUMMY_COURSES (
    COURSE_ID NUMBER PRIMARY KEY,
    COURSE_NAME VARCHAR2(100),
    FEES NUMBER(10, 2)
);

-- Insert data
INSERT INTO DUMMY_COURSES VALUES (1, 'Python', 5000);
INSERT INTO DUMMY_COURSES VALUES (2, 'Java', 6000);
COMMIT;
```

### 4. Run Query and Export

```bash
python main1.py --query "SELECT COURSE_NAME, COURSE_ID, FEES FROM DUMMY_COURSES" --excel report.xlsx
```

---

## 📝 Common Commands

### Basic Excel Export
```bash
python main1.py --query "SELECT * FROM DUMMY_COURSES" --excel courses.xlsx
```

### Export to Excel and PDF
```bash
python main1.py --query "SELECT * FROM DUMMY_COURSES" --excel courses.xlsx --pdf courses.pdf
```

### Export and Send Email
```bash
python main1.py \
  --query "SELECT * FROM DUMMY_COURSES" \
  --excel courses.xlsx \
  --send-email \
  --subject "Daily Report"
```

### Full Example (Excel + PDF + Email)
```bash
python main1.py \
  --query "SELECT COURSE_NAME, COURSE_ID, FEES FROM DUMMY_COURSES WHERE FEES > 5000" \
  --excel courses.xlsx \
  --pdf courses.pdf \
  --send-email \
  --subject "High-Value Courses Report"
```

---

## 🔧 Troubleshooting

**Error: ModuleNotFoundError: No module named 'oracledb'**
```bash
pip install oracledb
```

**Error: Oracle Client library not found**
- Install Oracle Instant Client
- macOS: `brew install instantclient-basic`
- Linux: Download from Oracle website
- Windows: Add to PATH

**Error: ORA-12154: TNS:could not resolve**
- Check ORACLE_HOST, ORACLE_PORT, ORACLE_SERVICE_NAME in .env
- Verify Oracle database is running

**Error: SMTP Authentication failed**
- For Gmail: Use App Password (not regular password)
- Enable 2-Step Verification first

---

## 📚 Full Documentation

See `ORACLE_SETUP_GUIDE.md` for complete setup instructions.

