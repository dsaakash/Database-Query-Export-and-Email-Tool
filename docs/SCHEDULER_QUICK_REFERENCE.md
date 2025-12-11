# Scheduler Quick Reference

Quick commands and examples for the task scheduler.

## 🚀 Quick Commands

```bash
# Add a new scheduled task
python manage_tasks.py add

# List all tasks
python manage_tasks.py list

# Show task details
python manage_tasks.py show <task-id>

# Enable a task
python manage_tasks.py enable <task-id>

# Disable a task
python manage_tasks.py disable <task-id>

# Delete a task
python manage_tasks.py delete <task-id>

# Start scheduler daemon
python scheduler_daemon.py
```

## 📅 Schedule Examples

### Cron Schedules

| Schedule | Configuration |
|----------|--------------|
| Daily at 9 AM | `hour=9, minute=0` |
| Every Monday 8:30 AM | `day_of_week=mon, hour=8, minute=30` |
| First of month midnight | `day=1, hour=0, minute=0` |
| Every hour | `minute=0` |
| Every 30 minutes | `minute=0,30` |
| Every weekday 9 AM | `day_of_week=mon-fri, hour=9, minute=0` |

### Interval Schedules

| Schedule | Configuration |
|----------|--------------|
| Every 1 hour | `hours=1` |
| Every 30 minutes | `minutes=30` |
| Every 15 minutes | `minutes=15` |
| Every 1 day | `days=1` |
| Every 1 week | `weeks=1` |

## 🔧 Free Cron Services

1. **Cron-Job.org** ⭐ (Recommended)
   - URL: https://cron-job.org
   - Free: Unlimited jobs, 1-min interval
   - Best for: Production use

2. **EasyCron**
   - URL: https://www.easycron.com
   - Free: 1 job, 1-hour interval
   - Best for: Simple use cases

3. **GitHub Actions**
   - Free: Unlimited for public repos
   - Best for: If using GitHub

4. **PythonAnywhere**
   - URL: https://www.pythonanywhere.com
   - Free: 1 always-on task
   - Best for: Python-focused projects

## 🖥️ Deployment Options

### Windows Task Scheduler (Windows 11) ⭐
- Use Windows built-in Task Scheduler
- Trigger: `python run_scheduled_tasks.py`
- See: [WINDOWS_TASK_SCHEDULER_SETUP.md](./WINDOWS_TASK_SCHEDULER_SETUP.md)

### Local Development (Daemon)
```bash
python scheduler_daemon.py
```

### VPS (systemd service)
```bash
sudo systemctl start db-scheduler
sudo systemctl status db-scheduler
```

### Cloud Platforms
- **Railway.app**: Connect GitHub, set env vars, deploy
- **Render.com**: Connect GitHub, set env vars, deploy
- **Heroku**: Use Heroku Scheduler addon

## 📝 Example Task Configuration

**Daily Sales Report:**
- Name: `Daily Sales Report`
- Query: `SELECT * FROM sales WHERE date = CURRENT_DATE`
- Schedule: Cron - `hour=9, minute=0`
- Recipients: `manager@company.com`
- Export: Excel enabled

**Hourly User Count:**
- Name: `Hourly User Count`
- Query: `SELECT COUNT(*) as user_count FROM users`
- Schedule: Interval - `hours=1`
- Recipients: `admin@company.com`
- Export: Excel enabled

## 🔍 Troubleshooting

```bash
# Check if scheduler is running
ps aux | grep scheduler_daemon

# View systemd logs
sudo journalctl -u db-scheduler -f

# Test task manually
python manage_tasks.py show <task-id>
```

## 📚 Full Documentation

See [SCHEDULER_GUIDE.md](./SCHEDULER_GUIDE.md) for complete documentation.

