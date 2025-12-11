# Task Scheduler Implementation Plan

Step-by-step guide on how the task scheduler was implemented and how to use it.

## 📋 Implementation Overview

The task scheduler system allows you to:
1. Schedule database queries to run automatically
2. Export results to Excel/PDF
3. Send email reports with attachments
4. Run continuously on a server
5. Use free cron services as triggers

---

## 🏗️ Architecture Components

### 1. **Task Model** (`src/core/task_model.py`)
   - Defines the structure of a scheduled task
   - Stores: query, schedule, email config, execution history
   - Uses dataclasses for clean data structure

### 2. **Task Storage** (`src/services/task_storage.py`)
   - Manages task persistence in JSON file (`tasks.json`)
   - CRUD operations: add, get, update, delete tasks
   - Tracks execution history and errors

### 3. **Scheduler Service** (`src/services/scheduler_service.py`)
   - Uses APScheduler library for scheduling
   - Executes tasks according to their schedules
   - Integrates with QueryService and EmailService
   - Handles errors and logging

### 4. **Scheduler Daemon** (`scheduler_daemon.py`)
   - Main process that runs continuously
   - Loads tasks from storage
   - Keeps scheduler running 24/7
   - Handles graceful shutdown

### 5. **Task Manager CLI** (`manage_tasks.py`)
   - Command-line interface for managing tasks
   - Commands: add, list, show, delete, enable, disable
   - Interactive prompts for task configuration

---

## 📝 Step-by-Step Implementation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**New dependency added:**
- `apscheduler>=3.10.0` - Advanced Python Scheduler library

### Step 2: Create a Scheduled Task

```bash
python manage_tasks.py add
```

**What happens:**
1. Prompts for task name and description
2. Asks for database connection (uses .env or manual entry)
3. Prompts for SQL query
4. Asks for schedule type (cron, interval, or once)
5. Configures schedule details
6. Sets up email recipients and subject
7. Configures export options (Excel/PDF)
8. Saves task to `tasks.json`

**Example:**
```
Task name: Daily Sales Report
Query: SELECT * FROM sales WHERE date = CURRENT_DATE
Schedule: Cron - Daily at 9 AM (hour=9, minute=0)
Recipients: manager@company.com
Export: Excel enabled
```

### Step 3: Start the Scheduler Daemon

```bash
python scheduler_daemon.py
```

**What happens:**
1. Loads all active tasks from `tasks.json`
2. Schedules each task using APScheduler
3. Runs continuously, executing tasks at scheduled times
4. Logs all executions and errors
5. Updates task run history

**Output:**
```
============================================================
Database Query Scheduler Daemon
============================================================
📋 Loading scheduled tasks...
✅ Loaded 1 active task(s):
   • Daily Sales Report (ID: abc12345...)
     Next run: 2024-12-20T09:00:00
============================================================
🔄 Scheduler is running. Waiting for scheduled tasks...
============================================================
```

### Step 4: Monitor Tasks

```bash
# List all tasks
python manage_tasks.py list

# View task details
python manage_tasks.py show <task-id>

# Check execution history
# (Last run, next run, error count shown in task details)
```

---

## 🌐 Deployment Options

### Option A: Local Development (Testing)

**Pros:**
- Easy to test
- No external dependencies
- Immediate feedback

**Cons:**
- Requires computer to be on 24/7
- Not suitable for production

**Usage:**
```bash
python scheduler_daemon.py
```

---

### Option B: Cloud VPS (Recommended for Production)

**Recommended Services:**
- DigitalOcean ($5/month)
- Linode ($5/month)
- Vultr ($5/month)
- AWS EC2 (pay-as-you-go)

**Setup Steps:**

1. **Deploy code to server:**
   ```bash
   git clone <your-repo>
   cd Database-Query-Export-and-Email-Tool
   pip install -r requirements.txt
   ```

2. **Create systemd service:**
   ```bash
   sudo nano /etc/systemd/system/db-scheduler.service
   ```

3. **Service configuration:**
   ```ini
   [Unit]
   Description=Database Query Scheduler
   After=network.target

   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/path/to/Database-Query-Export-and-Email-Tool
   ExecStart=/usr/bin/python3 /path/to/scheduler_daemon.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

4. **Enable and start:**
   ```bash
   sudo systemctl enable db-scheduler
   sudo systemctl start db-scheduler
   sudo systemctl status db-scheduler
   ```

5. **View logs:**
   ```bash
   sudo journalctl -u db-scheduler -f
   ```

---

### Option C: Free Cloud Platforms

#### Railway.app
- **URL**: https://railway.app
- **Free Tier**: $5 credit/month
- **Setup**: Connect GitHub, set env vars, deploy

#### Render.com
- **URL**: https://render.com
- **Free Tier**: Free web services
- **Setup**: Connect GitHub, set start command: `python scheduler_daemon.py`

#### PythonAnywhere
- **URL**: https://www.pythonanywhere.com
- **Free Tier**: 1 always-on task
- **Setup**: Upload code, create always-on task

---

### Option D: Free Cron Services (Hybrid Approach)

**Best Approach:** Run daemon on cloud + use free cron as backup trigger

#### 1. Cron-Job.org (Recommended) ⭐

**Why it's best:**
- ✅ Unlimited jobs (free tier)
- ✅ 1-minute minimum interval
- ✅ No credit card required
- ✅ Email notifications
- ✅ Execution history

**Setup:**
1. Create account at https://cron-job.org
2. Add new cron job
3. Set URL to your API endpoint (if you create one)
4. Configure schedule
5. Save and activate

**Alternative:** Use cron service to trigger a webhook that executes a specific task

#### 2. EasyCron
- **Free Tier**: 1 job, 1-hour minimum
- **URL**: https://www.easycron.com

#### 3. GitHub Actions (If using GitHub)
- **Free Tier**: Unlimited for public repos
- **Setup**: Create `.github/workflows/scheduler.yml`

**Example workflow:**
```yaml
name: Scheduled Task

on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC

jobs:
  run-task:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python -c "from src.services.scheduler_service import SchedulerService; s = SchedulerService(); s.load_all_tasks(); import time; time.sleep(60)"
```

---

## 🔄 How It Works (Technical Flow)

```
┌─────────────────────────────────────────────────────────┐
│                    Scheduler Daemon                      │
│                  (scheduler_daemon.py)                  │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ├─→ Loads tasks from tasks.json
                        │
                        ├─→ Schedules each task with APScheduler
                        │
                        └─→ Runs continuously
                             │
                             ├─→ When schedule triggers:
                             │   │
                             │   ├─→ Execute query via QueryService
                             │   │
                             │   ├─→ Export to Excel/PDF
                             │   │
                             │   ├─→ Send email via EmailService
                             │   │
                             │   └─→ Update task history
                             │
                             └─→ Log execution results
```

### Execution Flow:

1. **Task Scheduled** → APScheduler triggers at scheduled time
2. **Query Execution** → QueryService executes SQL query
3. **Export** → Results exported to Excel/PDF
4. **Email** → EmailService sends report with attachments
5. **Update History** → TaskStorage updates last_run, next_run, error_count

---

## 📊 Task Storage Format

Tasks are stored in `tasks.json`:

```json
[
  {
    "task_id": "abc-123-def-456",
    "name": "Daily Sales Report",
    "description": "Daily sales summary",
    "database_type": "postgresql",
    "database_url": "postgresql://...",
    "query": "SELECT * FROM sales WHERE date = CURRENT_DATE",
    "schedule_type": "cron",
    "schedule_config": {
      "hour": 9,
      "minute": 0
    },
    "email_recipients": ["manager@company.com"],
    "email_subject": "Daily Sales Report",
    "export_excel": true,
    "is_active": true,
    "created_at": "2024-12-19T10:00:00",
    "last_run": "2024-12-19T09:00:00",
    "next_run": "2024-12-20T09:00:00",
    "run_count": 5,
    "error_count": 0
  }
]
```

---

## 🎯 Recommended Deployment Strategy

### For Production:

1. **Deploy scheduler daemon to VPS** ($5/month)
   - DigitalOcean, Linode, or Vultr
   - Use systemd service for auto-restart
   - Runs 24/7, handles all scheduled tasks

2. **Use free cron service as backup** (Optional)
   - Cron-Job.org to trigger webhook
   - Provides redundancy
   - Can trigger specific tasks on-demand

3. **Monitor and maintain**
   - Check logs regularly
   - Monitor task execution
   - Update tasks as needed

### For Development/Testing:

1. **Run locally**
   ```bash
   python scheduler_daemon.py
   ```

2. **Test with short intervals**
   - Use 1-minute intervals for testing
   - Verify email delivery
   - Check execution logs

---

## 🔧 Maintenance

### Regular Tasks:

1. **Monitor execution logs**
   ```bash
   sudo journalctl -u db-scheduler -f
   ```

2. **Check task status**
   ```bash
   python manage_tasks.py list
   ```

3. **Review errors**
   ```bash
   python manage_tasks.py show <task-id>
   # Check "error_count" and "last_error" fields
   ```

4. **Update tasks as needed**
   ```bash
   python manage_tasks.py disable <task-id>  # Temporarily disable
   # Make changes
   python manage_tasks.py enable <task-id>  # Re-enable
   ```

### Backup:

- **Backup `tasks.json`** regularly (contains all task configurations)
- **Backup `.env`** file (contains credentials)

---

## 🚨 Troubleshooting

### Scheduler Not Running

**Check:**
```bash
# If using systemd
sudo systemctl status db-scheduler

# Check process
ps aux | grep scheduler_daemon

# View logs
sudo journalctl -u db-scheduler -n 50
```

### Tasks Not Executing

1. **Check task status:**
   ```bash
   python manage_tasks.py list
   ```
   Ensure tasks are "Active"

2. **Verify schedule:**
   ```bash
   python manage_tasks.py show <task-id>
   ```
   Check `next_run` field

3. **Check logs for errors**

### Email Not Sending

1. **Verify `.env` email configuration**
2. **Test email manually:**
   ```bash
   python test_email.py
   ```
3. **Check SMTP credentials**

---

## 📚 Next Steps

1. **Read full documentation:**
   - [SCHEDULER_GUIDE.md](./SCHEDULER_GUIDE.md) - Complete guide
   - [SCHEDULER_QUICK_REFERENCE.md](./SCHEDULER_QUICK_REFERENCE.md) - Quick commands

2. **Create your first task:**
   ```bash
   python manage_tasks.py add
   ```

3. **Start scheduler:**
   ```bash
   python scheduler_daemon.py
   ```

4. **Deploy to production:**
   - Choose deployment option
   - Set up systemd service (if VPS)
   - Monitor and maintain

---

**Happy Scheduling! 🚀**

