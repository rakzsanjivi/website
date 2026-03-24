# PythonAnywhere Deployment Guide

This guide will walk you through deploying your Django Portfolio to PythonAnywhere.com so it is live on the internet, 100% free.

## Part 1: Push Code to GitHub

Before deploying, your code must be stored securely on GitHub.

1. Create a free account at [github.com](https://github.com) if you don't have one.
2. Download and install [Git for Windows](https://gitforwindows.org/) (use default settings).
3. Go to GitHub and click **New Repository**. 
   - Name it `portfolio-django`
   - Make it **Private** or **Public** (your choice).
   - Do NOT check "Add a README file".
4. Open your local terminal in VS Code or PowerShell (make sure you are in `d:\HTML`). Run these exact commands, one by one:
   ```bash
   git init
   git add .
   git commit -m "First commit - Ready for Hosting"
   git branch -M main
   # Replace the URL below with YOUR actual GitHub repository URL!
   git remote add origin https://github.com/yourusername/portfolio-django.git
   git push -u origin main
   ```
*(If it prompts you to log into GitHub, do so).*

---

## Part 2: Set up PythonAnywhere

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com/) and click **Pricing & signup**. Create a free "Beginner" account. Your username will become your website URL (e.g., `raghavarajan.pythonanywhere.com`).
2. Once logged into the dashboard, click on **Consoles** -> **Bash** to open a cloud terminal.
3. In that terminal, copy your code from GitHub to their server:
   ```bash
   git clone https://github.com/yourusername/portfolio-django.git
   ```
   *(Always replace `yourusername` with your real one)*

4. Create a virtual environment and install your packages:
   ```bash
   mkvirtualenv --python=python3.10 myvenv
   cd portfolio-django
   pip install -r requirements.txt
   ```

5. Run the database setup commands on their server:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```
*(You will need to create a new admin username and password when prompted)*

---

## Part 3: Configure the Web Tab

1. Click the **PythonAnywhere Logo** in the top left to go back to the dashboard.
2. Go to the **Web** tab and click **Add a new web app**.
3. Click Next. **CRITICAL:** Do NOT choose Django here. Choose **Manual configuration** (including virtualenvs).
4. Choose **Python 3.10**. Click Next.

You are now on the configuration screen. Find these three sections and update them:

### A. Virtualenv
Scroll down to the "Virtualenv" section. Click the red text that says "Enter path to a virtualenv, if desired" and type:
```
/home/yourusername/.virtualenvs/myvenv
```
*(Hit enter to save in the box).*

### B. Code Directory
Scroll up slightly to "Source code". Click the directory path and type:
```
/home/yourusername/portfolio-django
```

### C. WSGI configuration file
Right below "Source code", there is a link for the **WSGI configuration file** (it looks like `/var/www/yourusername_pythonanywhere_com_wsgi.py`). Click it to edit the file.

Delete EVERYTHING in that file and paste this exact code:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/portfolio-django'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio_project.settings'
os.environ['DJANGO_DEBUG'] = 'False'

# Serve the Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Make sure to change `yourusername` in line 5)*. Click the **Save** button at the top right, then go back to the Web tab.

---

## Part 4: Launch It!

At the very top of the Web tab, click the giant green **Reload yourusername.pythonanywhere.com** button.

Click your website URL right above the reload button. Your Django portfolio should now be live on the internet! 

*(Try sending a test message through the contact form, then log into `yoursite.pythonanywhere.com/admin/` to verify it went through!)*
