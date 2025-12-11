# Windows Task Scheduler Setup Guide

Complete guide for using Windows 11 Task Scheduler to run automated database queries.

## 📋 Overview

Instead of running a continuous daemon, you can use Windows Task Scheduler to trigger your scheduled tasks at specific times. This is perfect for Windows users who want to:
- ✅ Avoid running a continuous background process
- ✅ Use Windows built-in scheduling
- ✅ Save system resources
- ✅ Have better control over when tasks run

---

## 🎯 How It Works

```
Windows Task Scheduler
    ↓ (triggers at scheduled time)
run_scheduled_tasks.py
    ↓ (loads all active tasks)
Execute tasks that are due
    ↓
Send email reports
```

**Key Difference:**
- **Daemon approach**: One process runs 24/7, executes tasks when scheduled
- **Windows Task Scheduler approach**: Windows triggers script at intervals, script executes all due tasks

---

## 📝 Step-by-Step Setup

### Step 1: Create Your Scheduled Tasks

First, create your scheduled tasks using the task manager:

```bash
python manage_tasks.py add
```

**Important:** When setting up tasks, use **interval schedules** or **cron schedules** that match how often you want Windows Task Scheduler to check for tasks.

**Example:**
- If you want to check every hour: Set Windows Task Scheduler to run every hour
- If you want daily reports: Set Windows Task Scheduler to run daily at 9 AM

### Step 2: Find Your Python Installation

You need the full path to your Python executable:

```bash
# In Command Prompt or PowerShell
where python
# or
python -c "import sys; print(sys.executable)"
```

**Common locations:**
- `C:\Python39\python.exe`
- `C:\Users\YourName\AppData\Local\Programs\Python\Python39\python.exe`
- `C:\Program Files\Python39\python.exe`

### Step 3: Create Windows Task Scheduler Task

#### Method A: Using GUI (Recommended)

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter
   - Or search "Task Scheduler" in Start menu

2. **Create Basic Task**
   - Click "Create Basic Task..." in the right panel
   - Name: `Database Query Scheduler`
   - Description: `Runs scheduled database queries and sends email reports`

3. **Set Trigger**
   - Choose trigger type:
     - **Daily**: For daily reports (e.g., every day at 9 AM)
     - **Weekly**: For weekly reports
     - **One time**: For one-time execution
     - **When the computer starts**: To run on startup
     - **When I log on**: To run when you log in
     - **When a specific event is logged**: Advanced option
   
   **For regular checks (recommended):**
   - Select **"Daily"**
   - Set time: `09:00:00` (or your preferred time)
   - Check "Recur every: 1 days"

4. **Set Action**
   - Select **"Start a program"**
   - **Program/script**: Full path to Python executable
     ```
     C:\Python39\python.exe
     ```
   - **Add arguments** (optional): 
     ```
     run_scheduled_tasks.py
     ```
   - **Start in**: Full path to your project directory
     ```
     D:\Database-Query-Export-and-Email-Tool
     ```

5. **Complete Setup**
   - Review settings
   - Check "Open the Properties dialog for this task when I click Finish"
   - Click Finish

6. **Configure Advanced Settings**
   - In Properties dialog:
     - **General tab**:
       - Check "Run whether user is logged on or not" (if you want it to run in background)
       - Check "Run with highest privileges" (if needed for database access)
       - Configure for: Windows 10/11
   
     - **Triggers tab**:
       - Edit trigger to set recurrence
       - For hourly checks: Change to "Daily", then set "Repeat task every: 1 hour"
       - Set duration: "Indefinitely" or specific end date
   
     - **Actions tab**:
       - Verify Python path and script path are correct
       - **Program/script**: `C:\Python39\python.exe`
       - **Add arguments**: `run_scheduled_tasks.py`
       - **Start in**: `D:\Database-Query-Export-and-Email-Tool`
   
     - **Conditions tab** (optional):
       - Uncheck "Start the task only if the computer is on AC power" (if using laptop)
       - Check "Wake the computer to run this task" (if needed)
   
     - **Settings tab**:
       - Check "Allow task to be run on demand"
       - Check "Run task as soon as possible after a scheduled start is missed"
       - Set "If the task fails, restart every: 10 minutes" (optional)
       - Set "Stop the task if it runs longer than: 1 hour" (optional)

7. **Test the Task**
   - Right-click the task → "Run"
   - Check if it executes successfully
   - View history in Task Scheduler

#### Method B: Using Command Line (PowerShell)

```powershell
# Create task that runs daily at 9 AM
$action = New-ScheduledTaskAction -Execute "C:\Python39\python.exe" -Argument "run_scheduled_tasks.py" -WorkingDirectory "D:\Database-Query-Export-and-Email-Tool"

$trigger = New-ScheduledTaskTrigger -Daily -At 9am

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "Database Query Scheduler" -Action $action -Trigger $trigger -Settings $settings -Description "Runs scheduled database queries and sends email reports"
```

**For hourly execution:**
```powershell
$action = New-ScheduledTaskAction -Execute "C:\Python39\python.exe" -Argument "run_scheduled_tasks.py" -WorkingDirectory "D:\Database-Query-Export-and-Email-Tool"

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 365)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "Database Query Scheduler Hourly" -Action $action -Trigger $trigger -Settings $settings -Description "Runs scheduled database queries every hour"
```

---

## 🔧 Common Configurations

### Configuration 1: Daily Reports at 9 AM

**Trigger:**
- Type: Daily
- Time: 09:00:00
- Recur every: 1 days

**Use case:** Daily sales reports, daily summaries

### Configuration 2: Hourly Checks

**Trigger:**
- Type: Daily
- Time: 00:00:00 (midnight)
- Recur every: 1 days
- **Advanced**: Repeat task every: 1 hour
- Duration: Indefinitely

**Use case:** Check for tasks every hour, execute any that are due

### Configuration 3: Every 15 Minutes

**Trigger:**
- Type: Daily
- Time: 00:00:00
- Recur every: 1 days
- **Advanced**: Repeat task every: 15 minutes
- Duration: Indefinitely

**Use case:** Frequent monitoring, real-time updates

### Configuration 4: Weekly Reports

**Trigger:**
- Type: Weekly
- Day: Monday
- Time: 09:00:00

**Use case:** Weekly summaries, Monday morning reports

---

## 📊 Task Management

### View Task Status

1. Open Task Scheduler
2. Navigate to "Task Scheduler Library"
3. Find your task: "Database Query Scheduler"
4. View:
   - **Status**: Ready/Running
   - **Last Run Time**: When it last executed
   - **Last Run Result**: Success (0x0) or error code
   - **Next Run Time**: When it will run next

### Run Task Manually

1. Right-click the task
2. Select "Run"
3. Check execution in "History" tab

### Edit Task

1. Right-click the task
2. Select "Properties"
3. Modify triggers, actions, or settings
4. Click OK

### Disable/Enable Task

1. Right-click the task
2. Select "Disable" or "Enable"

### Delete Task

1. Right-click the task
2. Select "Delete"
3. Confirm deletion

---

## 🔍 Monitoring and Logging

### View Execution History

1. Open Task Scheduler
2. Select your task
3. Click "History" tab
4. View:
   - Execution times
   - Success/failure status
   - Error messages (if any)

### Check Script Output

The script outputs to console. To capture logs:

**Option 1: Redirect to file in Task Scheduler**

In Task Properties → Actions:
- **Add arguments**: `run_scheduled_tasks.py >> logs.txt 2>&1`

**Option 2: Create a wrapper batch file**

Create `run_tasks_with_logging.bat`:
```batch
@echo off
cd /d D:\Database-Query-Export-and-Email-Tool
python run_scheduled_tasks.py >> logs\task_log_%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt 2>&1
```

Then in Task Scheduler:
- **Program/script**: `D:\Database-Query-Export-and-Email-Tool\run_tasks_with_logging.bat`

---

## 🎯 Best Practices

### 1. Schedule Windows Task to Run Frequently

Since Windows Task Scheduler triggers the script, set it to run:
- **Every hour**: If you have hourly tasks
- **Every 15-30 minutes**: For more frequent checks
- **Daily at specific time**: For daily reports only

### 2. Configure Task Schedules in Your Tasks

When creating tasks with `manage_tasks.py add`:
- Use **interval schedules** that match your Windows Task Scheduler frequency
- Example: If Windows Task runs every hour, set task intervals to 1 hour, 2 hours, etc.

### 3. Use Appropriate Triggers

- **Daily at specific time**: For reports that need to run at exact times
- **Hourly**: For tasks that can run any time within the hour
- **On startup**: For initialization tasks

### 4. Test Before Production

1. Create a test task with short interval
2. Run Windows Task manually
3. Verify email delivery
4. Check logs
5. Then schedule for production

### 5. Monitor Regularly

- Check Task Scheduler history weekly
- Review error logs
- Verify emails are being sent
- Update tasks as needed

---

## 🚨 Troubleshooting

### Task Not Running

**Check:**
1. Task status in Task Scheduler (should be "Ready")
2. Last run result (should be 0x0 for success)
3. Task is enabled (not disabled)
4. User account has permissions

**Fix:**
- Right-click task → Run (test manually)
- Check "History" tab for errors
- Verify Python path is correct
- Check "Run whether user is logged on or not" setting

### Script Executes But No Tasks Run

**Check:**
1. Tasks exist: `python manage_tasks.py list`
2. Tasks are active: `python manage_tasks.py show <task-id>`
3. Schedule configuration is correct

**Fix:**
- Verify tasks are marked as "Active"
- Check task schedules match Windows Task Scheduler frequency
- Review task details: `python manage_tasks.py show <task-id>`

### Python Not Found Error

**Error:** `The system cannot find the file specified`

**Fix:**
1. Verify Python path in Task Scheduler
2. Use full path: `C:\Python39\python.exe`
3. Test path in Command Prompt:
   ```cmd
   "C:\Python39\python.exe" --version
   ```

### Import Errors

**Error:** `ModuleNotFoundError` or import errors

**Fix:**
1. Ensure "Start in" directory is set correctly
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Use full Python path with virtual environment if using one

### Email Not Sending

**Check:**
1. `.env` file has correct email configuration
2. SMTP credentials are valid
3. Test email manually: `python test_email.py`

**Fix:**
- Verify `.env` file exists in project root
- Check SMTP settings
- Test email configuration

---

## 📋 Example: Complete Setup

### Scenario: Daily Sales Report at 9 AM

1. **Create task:**
   ```bash
   python manage_tasks.py add
   ```
   - Name: Daily Sales Report
   - Query: `SELECT * FROM sales WHERE date = CURRENT_DATE`
   - Schedule: Interval - 1 day (or cron - daily at 9 AM)
   - Recipients: manager@company.com

2. **Create Windows Task:**
   - Name: Database Query Scheduler
   - Trigger: Daily at 9:00 AM
   - Action: Run `python.exe` with argument `run_scheduled_tasks.py`
   - Start in: Project directory

3. **Test:**
   - Right-click task → Run
   - Check email delivery
   - Verify in Task Scheduler history

4. **Monitor:**
   - Check Task Scheduler history daily
   - Review logs if issues occur

---

## 🔄 Comparison: Daemon vs Windows Task Scheduler

| Feature | Daemon Approach | Windows Task Scheduler |
|---------|----------------|----------------------|
| **Resource Usage** | Continuous process | Runs only when triggered |
| **Setup Complexity** | Simple | Moderate |
| **Windows Native** | No | Yes |
| **Flexibility** | High (any schedule) | High (any schedule) |
| **Monitoring** | Logs | Task Scheduler UI |
| **Best For** | Linux/Cloud servers | Windows desktops/servers |

**Recommendation:**
- **Windows desktop/server**: Use Windows Task Scheduler
- **Linux/Cloud**: Use daemon approach
- **Both**: Can use either, choose based on preference

---

## 📚 Additional Resources

- **Windows Task Scheduler Documentation**: https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page
- **Task Scheduler PowerShell Cmdlets**: https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/

---

## ✅ Quick Checklist

- [ ] Python installed and path verified
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Tasks created: `python manage_tasks.py add`
- [ ] Tasks verified: `python manage_tasks.py list`
- [ ] Windows Task Scheduler task created
- [ ] Task tested manually (right-click → Run)
- [ ] Email configuration verified in `.env`
- [ ] Test email sent successfully
- [ ] Task scheduled and enabled
- [ ] Monitoring setup (check history/logs)

---

**You're all set! Your scheduled tasks will now run automatically using Windows Task Scheduler! 🎉**

