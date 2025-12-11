# Task Scheduler Guide

Complete guide for scheduling database queries and automated email reports.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Free Cron Services](#free-cron-services)
5. [Deployment Options](#deployment-options)
6. [Step-by-Step Setup](#step-by-step-setup)
7. [Managing Tasks](#managing-tasks)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The Task Scheduler allows you to:
- ✅ Schedule database queries to run automatically
- ✅ Export results to Excel/PDF
- ✅ Send email reports with attachments
- ✅ Run tasks on cron schedules, intervals, or one-time
- ✅ Track task execution history and errors

---

## Architecture

```
┌─────────────────┐
│  Scheduler      │
│   Daemon        │  ← Runs continuously
└────────┬────────┘
         │
         ├─→ Loads tasks from tasks.json
         │
         ├─→ Executes queries via QueryService
         │
         └─→ Sends emails via EmailService
```

**Components:**
- `scheduler_daemon.py` - Main daemon that runs continuously
- `manage_tasks.py` - CLI for managing scheduled tasks
- `TaskStorage` - Stores tasks in JSON file (`tasks.json`)
- `SchedulerService` - Uses APScheduler to execute tasks
- `QueryService` - Executes queries and exports results

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add a Scheduled Task

```bash
python manage_tasks.py add
```

Follow the prompts to configure:
- Task name and description
- Database connection
- SQL query
- Schedule (cron, interval, or once)
- Email recipients
- Export options

### 3. Start the Scheduler Daemon

```bash
python scheduler_daemon.py
```

The daemon will:
- Load all active tasks
- Execute them according to their schedules
- Run continuously until stopped (Ctrl+C)

---

## Free Cron Services

For production deployments, you can use free cron services to trigger your scheduler. Here are the best options:

### 1. **Cron-Job.org** ⭐ Recommended
- **URL**: https://cron-job.org
- **Free Tier**: Unlimited jobs, 1-minute minimum interval
- **Features**:
  - HTTP requests to trigger your API
  - Email notifications on failures
  - Execution history
  - No credit card required

**Setup:**
1. Create account at cron-job.org
2. Add new cron job
3. Set URL to: `https://your-server.com/api/trigger-scheduler`
4. Configure schedule
5. Save and activate

### 2. **EasyCron**
- **URL**: https://www.easycron.com
- **Free Tier**: 1 job, 1-hour minimum interval
- **Features**:
  - Simple interface
  - Email alerts
  - Execution logs

### 3. **UptimeRobot** (for monitoring + cron)
- **URL**: https://uptimerobot.com
- **Free Tier**: 50 monitors, 5-minute interval
- **Features**:
  - HTTP monitoring
  - Can trigger webhooks
  - Email/SMS alerts

### 4. **GitHub Actions** (if using GitHub)
- **Free Tier**: Unlimited for public repos, 2000 minutes/month for private
- **Features**:
  - YAML-based configuration
  - Integrated with code
  - Free for public repositories

**Example GitHub Actions workflow:**
```yaml
name: Scheduled Database Report

on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  run-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run scheduled task
        run: python -c "from src.services.scheduler_service import SchedulerService; s = SchedulerService(); s.load_all_tasks(); import time; time.sleep(60)"
```

### 5. **PythonAnywhere** (Free tier)
- **URL**: https://www.pythonanywhere.com
- **Free Tier**: 1 always-on task
- **Features**:
  - Host Python scripts
  - Built-in scheduler
  - Free tier available

---

## Deployment Options

### Option 1: Windows Task Scheduler (Recommended for Windows) ⭐

Use Windows 11 built-in Task Scheduler to trigger tasks:

```bash
# Create tasks
python manage_tasks.py add

# Windows Task Scheduler will trigger:
python run_scheduled_tasks.py
```

**Setup:**
1. Create tasks using `manage_tasks.py add`
2. Configure Windows Task Scheduler to run `run_scheduled_tasks.py` at your desired intervals
3. Windows handles the scheduling - no daemon needed!

**Pros:**
- ✅ Native Windows integration
- ✅ No continuous process running
- ✅ Built-in monitoring via Task Scheduler UI
- ✅ Saves system resources
- ✅ Easy to manage via Windows GUI

**See:** [WINDOWS_TASK_SCHEDULER_SETUP.md](./WINDOWS_TASK_SCHEDULER_SETUP.md) for complete setup guide.

---

### Option 2: Local Server (Development/Testing)

Run the daemon on your local machine:

```bash
# Terminal 1: Start scheduler
python scheduler_daemon.py

# Terminal 2: Manage tasks
python manage_tasks.py list
```

**Pros:**
- Easy to test
- No external dependencies

**Cons:**
- Requires computer to be on 24/7
- Not suitable for production

---

### Option 2: Cloud Server (Recommended for Production)

Deploy to a cloud server that runs 24/7:

#### A. **VPS (DigitalOcean, Linode, Vultr)**
- **Cost**: $5-10/month
- **Setup**:
  ```bash
  # Install Python and dependencies
  sudo apt update
  sudo apt install python3 python3-pip
  pip3 install -r requirements.txt
  
  # Create systemd service
  sudo nano /etc/systemd/system/db-scheduler.service
  ```

  **Service file** (`/etc/systemd/system/db-scheduler.service`):
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

  **Enable and start:**
  ```bash
  sudo systemctl enable db-scheduler
  sudo systemctl start db-scheduler
  sudo systemctl status db-scheduler
  ```

#### B. **Heroku** (Free tier discontinued, but paid options available)
- **Cost**: $7/month (Eco dyno)
- **Setup**: Use Heroku Scheduler addon

#### C. **Railway.app** (Free tier available)
- **URL**: https://railway.app
- **Free Tier**: $5 credit/month
- **Features**: Auto-deploy from GitHub

#### D. **Render.com** (Free tier available)
- **URL**: https://render.com
- **Free Tier**: Free web services (with limitations)
- **Features**: Easy deployment

---

### Option 3: Serverless Functions

Deploy as serverless function (triggered by cron service):

#### A. **Vercel** (Free tier)
- **URL**: https://vercel.com
- **Free Tier**: Generous free tier
- **Setup**: Deploy Python function

#### B. **AWS Lambda** (Free tier)
- **Free Tier**: 1 million requests/month
- **Setup**: Use EventBridge for scheduling

#### C. **Google Cloud Functions** (Free tier)
- **Free Tier**: 2 million invocations/month
- **Setup**: Use Cloud Scheduler

---

### Option 4: Hybrid Approach (Recommended)

**Best of both worlds:**

1. **Run scheduler daemon on cloud server** (VPS, Railway, etc.)
   - Handles all scheduled tasks
   - Runs 24/7
   - Cost: $5-10/month

2. **Use free cron service as backup/trigger**
   - Cron-Job.org calls your API endpoint
   - API endpoint triggers immediate task execution
   - Provides redundancy

**API Endpoint Example** (`api_trigger.py`):
```python
from flask import Flask, request
from src.services.scheduler_service import SchedulerService
from src.services.task_storage import TaskStorage

app = Flask(__name__)
scheduler = SchedulerService()

@app.route('/trigger-task/<task_id>', methods=['POST'])
def trigger_task(task_id):
    # Verify API key from request
    api_key = request.headers.get('X-API-Key')
    if api_key != os.getenv('API_KEY'):
        return {'error': 'Unauthorized'}, 401
    
    # Execute task immediately
    storage = TaskStorage()
    task = storage.get_task(task_id)
    if task:
        scheduler._execute_task(task)
        return {'success': True, 'task_id': task_id}
    return {'error': 'Task not found'}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## Step-by-Step Setup

### Step 1: Install Dependencies

```bash
cd Database-Query-Export-and-Email-Tool
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create/update `.env` file:

```env
# Database
POSTGRESQL_DATABASE_URL=postgresql://user:pass@host:port/dbname

# Email
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

# Optional: API Key for webhook triggers
API_KEY=your-secret-api-key
```

### Step 3: Create Your First Scheduled Task

```bash
python manage_tasks.py add
```

**Example configuration:**
- **Name**: Daily Sales Report
- **Query**: `SELECT * FROM sales WHERE date = CURRENT_DATE`
- **Schedule**: Cron - Daily at 9 AM (hour=9, minute=0)
- **Recipients**: manager@company.com
- **Export**: Excel enabled

### Step 4: Test the Task

```bash
# List tasks
python manage_tasks.py list

# View task details
python manage_tasks.py show <task-id>

# Start scheduler (test run)
python scheduler_daemon.py
```

### Step 5: Deploy to Production

Choose your deployment option (see [Deployment Options](#deployment-options)):

**For VPS (systemd service):**
```bash
# Create service file
sudo nano /etc/systemd/system/db-scheduler.service
# (paste service configuration from above)

# Enable and start
sudo systemctl enable db-scheduler
sudo systemctl start db-scheduler

# Check status
sudo systemctl status db-scheduler

# View logs
sudo journalctl -u db-scheduler -f
```

**For Railway/Render:**
1. Connect GitHub repository
2. Set environment variables
3. Set start command: `python scheduler_daemon.py`
4. Deploy

---

## Managing Tasks

### Add Task
```bash
python manage_tasks.py add
```

### List All Tasks
```bash
python manage_tasks.py list
```

### View Task Details
```bash
python manage_tasks.py show <task-id>
```

### Disable Task (temporarily)
```bash
python manage_tasks.py disable <task-id>
```

### Enable Task
```bash
python manage_tasks.py enable <task-id>
```

### Delete Task
```bash
python manage_tasks.py delete <task-id>
```

---

## Schedule Types

### 1. Cron Schedule

**Examples:**

| Description | Configuration |
|------------|---------------|
| Daily at 9 AM | `hour=9, minute=0` |
| Every Monday at 8:30 AM | `day_of_week='mon', hour=8, minute=30` |
| First day of month at midnight | `day=1, hour=0, minute=0` |
| Every hour | `minute=0` |
| Every 30 minutes | `minute=0,30` |

### 2. Interval Schedule

**Examples:**

| Description | Configuration |
|------------|---------------|
| Every 1 hour | `hours=1` |
| Every 30 minutes | `minutes=30` |
| Every 1 day | `days=1` |
| Every 1 week | `weeks=1` |

### 3. One-Time Schedule

**Format**: `YYYY-MM-DD HH:MM:SS`

**Example**: `2024-12-25 09:00:00`

---

## Troubleshooting

### Scheduler Not Running

**Check:**
```bash
# If using systemd
sudo systemctl status db-scheduler
sudo journalctl -u db-scheduler -n 50

# Check if process is running
ps aux | grep scheduler_daemon
```

### Tasks Not Executing

1. **Check task status:**
   ```bash
   python manage_tasks.py list
   ```
   Ensure tasks are marked as "Active"

2. **Check logs:**
   - Scheduler daemon logs will show execution attempts
   - Check for errors in task execution

3. **Verify schedule:**
   ```bash
   python manage_tasks.py show <task-id>
   ```
   Check `next_run` field

### Email Not Sending

1. **Verify email configuration in `.env`**
2. **Test email manually:**
   ```bash
   python test_email.py
   ```
3. **Check SMTP credentials and app password**

### Database Connection Issues

1. **Verify database URL in `.env`**
2. **Test connection:**
   ```bash
   python main.py
   ```
3. **Check network/firewall settings**

---

## Best Practices

1. **Start with test tasks** - Use short intervals for testing
2. **Monitor first few runs** - Check logs and email delivery
3. **Use descriptive task names** - Makes management easier
4. **Set up error notifications** - Monitor task failures
5. **Backup tasks.json** - Contains all task configurations
6. **Use environment variables** - Never hardcode credentials
7. **Test queries first** - Run queries manually before scheduling
8. **Set appropriate schedules** - Don't overload database

---

## Security Considerations

1. **Protect `.env` file** - Never commit to version control
2. **Use API keys** - If exposing API endpoints
3. **Limit database permissions** - Use read-only user if possible
4. **Secure email credentials** - Use app passwords, not main passwords
5. **Monitor access logs** - Check for unauthorized access

---

## Support

For issues or questions:
1. Check logs: `sudo journalctl -u db-scheduler -f`
2. Review task details: `python manage_tasks.py show <task-id>`
3. Test components individually (database, email, queries)

---

**Happy Scheduling! 🚀**

