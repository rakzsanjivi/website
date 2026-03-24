# Django Contact Form Backend – Complete Setup Guide

This guide covers the full process of hosting your HTML portfolio with Django **and** connecting your contact form to a Python backend so you can receive messages.

---

## Prerequisites
- Python installed on your system
- Your existing HTML portfolio files in `d:\HTML`

---

## Part 1: Django Project Setup

### Step 1: Install Django
```powershell
pip install django
```

### Step 2: Create the Django Project
```powershell
cd d:\HTML
django-admin startproject portfolio_project .
```
> The `.` creates `manage.py` directly inside `d:\HTML`.

### Step 3: Configure `portfolio_project/settings.py`

**A. Point Templates to your root folder** — find the `TEMPLATES` list and update `DIRS`:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],   # <--- serves index.html from d:\HTML
        ...
    },
]
```

**B. Point Static Files to your root folder** — at the bottom of the file, add:
```python
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR,
]
```

**C. Register the contact app** — add `'contact'` to the `INSTALLED_APPS` list:
```python
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
    'contact',   # <--- add this
]
```

### Step 4: Configure `portfolio_project/urls.py`
Replace the contents with:
```python
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render
from django.conf import settings
from django.views.static import serve
import os

def home_view(request):
    return render(request, 'index.html')

def serve_root_file(request, filepath):
    return serve(request, filepath, document_root=settings.BASE_DIR)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', include('contact.urls')),
    path('', home_view, name='home'),
]

# In development, serve static files (CSS, JS, images) directly from BASE_DIR
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^(?P<filepath>css/.*)$', serve_root_file),
        re_path(r'^(?P<filepath>js/.*)$', serve_root_file),
        re_path(r'^(?P<filepath>img/.*)$', serve_root_file),
        re_path(r'^(?P<filepath>assets/.*)$', serve_root_file),
        re_path(r'^(?P<filepath>style\.css)$', serve_root_file),
    ]
```

---

## Part 2: Creating the Contact App

### Step 5: Create the App
```powershell
python manage.py startapp contact
```

### Step 6: Define the Model (`contact/models.py`)
This creates a database table to store every message people send you:
```python
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at:%Y-%m-%d %H:%M})"
```

### Step 7: Create the View (`contact/views.py`)
This handles the incoming form data (as JSON) and saves it to the database:
```python
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ContactMessage

@csrf_exempt
@require_POST
def submit_contact(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

        ContactMessage.objects.create(name=name, email=email, message=message)
        return JsonResponse({'status': 'success', 'message': 'Your message has been sent successfully!'})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data format.'}, status=400)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Something went wrong.'}, status=500)
```

### Step 8: Create the URL Route (`contact/urls.py`)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_contact, name='submit_contact'),
]
```

### Step 9: Register in Admin (`contact/admin.py`)
This lets you view all received messages in the Django Admin dashboard:
```python
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    ordering = ('-created_at',)
```

---

## Part 3: Updating the HTML Form

### Step 10: Update Contact Form in `index.html`
Replace the existing contact form with this AJAX-powered version:
```html
<!-- Alert Banner (hidden by default) -->
<div id="form-alert" style="display:none; padding: 15px 20px; border-radius: 10px; margin-bottom: 16px; font-size: 15px; font-weight: 500;">
    <span id="form-alert-text"></span>
    <button onclick="document.getElementById('form-alert').style.display='none'" style="background:none; border:none; color:inherit; font-size:18px; cursor:pointer;">&times;</button>
</div>

<form id="contact-form" class="contact-form glass-card">
    <div class="form-group">
        <input type="text" id="contact-name" placeholder="Your Name" required>
    </div>
    <div class="form-group">
        <input type="email" id="contact-email" placeholder="Your Email" required>
    </div>
    <div class="form-group">
        <textarea id="contact-message" placeholder="Your Message" required></textarea>
    </div>
    <button type="submit" id="contact-submit-btn" class="btn btn-primary">
        Send Message <i class="fas fa-paper-plane"></i>
    </button>
</form>
```

### Step 11: Add AJAX Script (before `</body>`)
```html
<script>
document.getElementById('contact-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const alertBox = document.getElementById('form-alert');
    const alertText = document.getElementById('form-alert-text');
    const submitBtn = document.getElementById('contact-submit-btn');

    const name = document.getElementById('contact-name').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const message = document.getElementById('contact-message').value.trim();

    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Sending... <i class="fas fa-spinner fa-spin"></i>';

    try {
        const response = await fetch('/contact/submit/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
        });
        const data = await response.json();

        alertBox.style.display = 'block';
        if (data.status === 'success') {
            alertBox.style.background = 'linear-gradient(135deg, #00c851, #007e33)';
            alertBox.style.color = '#fff';
            alertText.textContent = data.message;
            document.getElementById('contact-form').reset();
        } else {
            alertBox.style.background = 'linear-gradient(135deg, #ff4444, #cc0000)';
            alertBox.style.color = '#fff';
            alertText.textContent = data.message;
        }
    } catch (error) {
        alertBox.style.display = 'block';
        alertBox.style.background = 'linear-gradient(135deg, #ff4444, #cc0000)';
        alertBox.style.color = '#fff';
        alertText.textContent = 'Network error. Please try again.';
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Send Message <i class="fas fa-paper-plane"></i>';
    }
    setTimeout(() => { alertBox.style.display = 'none'; }, 6000);
});
</script>
```

---

## Part 4: Run Migrations & Start the Server

### Step 12: Create the Database Tables
```powershell
python manage.py makemigrations contact
python manage.py migrate
```

### Step 13: Create an Admin User (to view messages)
```powershell
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### Step 14: Start the Development Server
```powershell
python manage.py runserver
```

---

## How to Use

| What                         | URL                             |
|------------------------------|---------------------------------|
| View your portfolio          | http://127.0.0.1:8000/          |
| View received messages       | http://127.0.0.1:8000/admin/    |
| Contact form API endpoint    | POST http://127.0.0.1:8000/contact/submit/ |

### Viewing Messages
1. Go to **http://127.0.0.1:8000/admin/**
2. Log in with your superuser credentials
3. Click on **Contact messages** to see all messages people have submitted, with their name, email, message, and timestamp.
