# End-to-End Testing Guide for Portfolio Website

This guide outlines how to test your Django-powered portfolio website from top to bottom before hosting it in production.

---

## Prerequisites
```powershell
pip install selenium pytest pytest-django
```
Also download [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version and add it to your system PATH.

---

## Part 1: Unit Tests (Backend Logic)

Unit tests verify that individual backend functions work correctly in isolation.

### Step 1: Create Test File
Create `d:\HTML\contact\tests.py`:
```python
import json
from django.test import TestCase, Client
from contact.models import ContactMessage


class ContactModelTest(TestCase):
    """Test the ContactMessage model."""

    def test_create_message(self):
        msg = ContactMessage.objects.create(
            name="John", email="john@example.com", message="Hello!"
        )
        self.assertEqual(msg.name, "John")
        self.assertEqual(msg.email, "john@example.com")
        self.assertEqual(str(msg), f"John - john@example.com ({msg.created_at:%Y-%m-%d %H:%M})")

    def test_ordering(self):
        msg1 = ContactMessage.objects.create(name="A", email="a@test.com", message="First")
        msg2 = ContactMessage.objects.create(name="B", email="b@test.com", message="Second")
        messages = list(ContactMessage.objects.all())
        self.assertEqual(messages[0].name, "B")  # Newest first


class ContactViewTest(TestCase):
    """Test the contact form submission endpoint."""

    def setUp(self):
        self.client = Client()
        self.url = '/contact/submit/'

    def test_valid_submission(self):
        response = self.client.post(self.url,
            data=json.dumps({"name": "Test", "email": "test@test.com", "message": "Hi"}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_missing_fields(self):
        response = self.client.post(self.url,
            data=json.dumps({"name": "", "email": "test@test.com", "message": "Hi"}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_invalid_json(self):
        response = self.client.post(self.url,
            data="not json",
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RAGHAVARAJAN')
```

### Step 2: Run Unit Tests
```powershell
cd d:\HTML
python manage.py test contact -v 2
```
Expected output: All tests should show `OK`.

---

## Part 2: End-to-End Tests (Browser Automation with Selenium)

E2E tests simulate a real user interacting with your website in a browser.

### Step 3: Create E2E Test File
Create `d:\HTML\tests_e2e.py`:
```python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000"


def setup_driver():
    """Initialize Chrome in headed mode so you can watch the tests."""
    options = webdriver.ChromeOptions()
    # Remove the line below if you want to see the browser window
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    return driver


def test_homepage_loads(driver):
    """Test 1: Homepage loads and shows the correct title."""
    driver.get(BASE_URL)
    assert "RAGHAVARAJAN" in driver.title, f"Expected 'RAGHAVARAJAN' in title, got: {driver.title}"
    print("✅ Test 1 PASSED: Homepage loads with correct title")


def test_navigation_links(driver):
    """Test 2: All nav links exist and scroll to sections."""
    driver.get(BASE_URL)
    sections = ["about", "skills", "projects", "education", "contact"]
    for section in sections:
        link = driver.find_element(By.CSS_SELECTOR, f'a[href="#{section}"]')
        assert link is not None, f"Nav link for #{section} not found"
    print("✅ Test 2 PASSED: All navigation links present")


def test_sections_exist(driver):
    """Test 3: All main sections are present on the page."""
    driver.get(BASE_URL)
    for section_id in ["hero", "about", "skills", "projects", "education", "contact"]:
        section = driver.find_element(By.ID, section_id)
        assert section is not None, f"Section #{section_id} not found"
    print("✅ Test 3 PASSED: All sections exist on the page")


def test_contact_form_success(driver):
    """Test 4: Contact form submits successfully and shows green alert."""
    driver.get(BASE_URL + "/#contact")
    time.sleep(1)

    # Fill in the form
    driver.find_element(By.ID, "contact-name").send_keys("Selenium Test")
    driver.find_element(By.ID, "contact-email").send_keys("selenium@test.com")
    driver.find_element(By.ID, "contact-message").send_keys("Automated test message")

    # Click submit
    driver.find_element(By.ID, "contact-submit-btn").click()
    time.sleep(2)

    # Check for success alert
    alert = driver.find_element(By.ID, "form-alert")
    assert alert.is_displayed(), "Alert banner did not appear"
    alert_text = driver.find_element(By.ID, "form-alert-text").text
    assert "success" in alert_text.lower(), f"Expected success message, got: {alert_text}"
    print("✅ Test 4 PASSED: Contact form submits and shows success alert")


def test_contact_form_clears_after_submit(driver):
    """Test 5: Form fields clear after successful submission."""
    driver.get(BASE_URL + "/#contact")
    time.sleep(1)

    name_field = driver.find_element(By.ID, "contact-name")
    email_field = driver.find_element(By.ID, "contact-email")
    msg_field = driver.find_element(By.ID, "contact-message")

    name_field.send_keys("Clear Test")
    email_field.send_keys("clear@test.com")
    msg_field.send_keys("Should clear after submit")

    driver.find_element(By.ID, "contact-submit-btn").click()
    time.sleep(2)

    assert name_field.get_attribute("value") == "", "Name field did not clear"
    assert email_field.get_attribute("value") == "", "Email field did not clear"
    assert msg_field.get_attribute("value") == "", "Message field did not clear"
    print("✅ Test 5 PASSED: Form fields clear after successful submission")


def test_responsive_mobile(driver):
    """Test 6: Site renders properly at mobile width."""
    driver.set_window_size(375, 812)  # iPhone X dimensions
    driver.get(BASE_URL)
    time.sleep(1)

    body = driver.find_element(By.TAG_NAME, "body")
    assert body.size['width'] <= 375, "Page is wider than mobile viewport"
    print("✅ Test 6 PASSED: Site fits mobile viewport")
    driver.set_window_size(1400, 900)  # Reset


def test_admin_login(driver):
    """Test 7: Django admin panel is accessible and login works."""
    driver.get(BASE_URL + "/admin/")
    time.sleep(1)

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    time.sleep(2)

    assert "Site administration" in driver.page_source, "Admin login failed"
    print("✅ Test 7 PASSED: Admin login works")


def test_messages_in_admin(driver):
    """Test 8: Submitted messages appear in admin panel."""
    # First submit a message
    driver.get(BASE_URL + "/#contact")
    time.sleep(1)
    driver.find_element(By.ID, "contact-name").send_keys("Admin Check")
    driver.find_element(By.ID, "contact-email").send_keys("admin@check.com")
    driver.find_element(By.ID, "contact-message").send_keys("Verify in admin")
    driver.find_element(By.ID, "contact-submit-btn").click()
    time.sleep(2)

    # Now check admin
    driver.get(BASE_URL + "/admin/contact/contactmessage/")
    time.sleep(1)

    # Login if needed
    if "login" in driver.current_url:
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        time.sleep(2)

    assert "Admin Check" in driver.page_source, "Submitted message not found in admin"
    print("✅ Test 8 PASSED: Messages visible in admin panel")


# ─── Run All Tests ───
if __name__ == "__main__":
    driver = setup_driver()
    tests = [
        test_homepage_loads,
        test_navigation_links,
        test_sections_exist,
        test_contact_form_success,
        test_contact_form_clears_after_submit,
        test_responsive_mobile,
        test_admin_login,
        test_messages_in_admin,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test(driver)
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print(f"{'='*50}")

    driver.quit()
```

### Step 4: Run E2E Tests
Make sure your Django server is running in one terminal:
```powershell
python manage.py runserver
```
Then open a **second terminal** and run:
```powershell
cd d:\HTML
python tests_e2e.py
```
A Chrome window will open and you'll see the tests run in real-time.

---

## Part 3: Performance Testing (Lighthouse)

Lighthouse is built into Chrome — no installation needed.

### Step 5: Run Lighthouse Audit
1. Open `http://127.0.0.1:8000/` in Chrome
2. Press `F12` to open DevTools
3. Click the **Lighthouse** tab
4. Select categories: Performance, Accessibility, Best Practices, SEO
5. Click **Analyze page load**
6. Review the scores (aim for 90+ on each)

### Key Metrics to Check
| Metric | Target | What it Measures |
|--------|--------|-----------------|
| Performance | 90+ | Page load speed |
| Accessibility | 90+ | Screen reader compatibility |
| Best Practices | 90+ | Modern web standards |
| SEO | 90+ | Search engine optimization |

---

## Part 4: Manual Testing Checklist

Run through this checklist before deploying:

### Layout & Visuals
- [ ] Homepage loads without errors
- [ ] All sections scroll smoothly when nav links are clicked
- [ ] Profile image / hero section displays correctly
- [ ] Glass-card effects render properly
- [ ] Animations and transitions work (fade-in, hover effects)

### Contact Form
- [ ] Form submits successfully with valid data
- [ ] Green success alert appears after submission
- [ ] Form fields clear after successful submission
- [ ] Error alert appears when fields are empty
- [ ] Button shows spinner while submitting

### Responsive Design
- [ ] Test on desktop (1920×1080)
- [ ] Test on tablet (768×1024)
- [ ] Test on mobile (375×812)
- [ ] Hamburger menu works on mobile
- [ ] Text is readable at all sizes

### Cross-Browser
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari (if on Mac)

### Admin Panel
- [ ] Admin login works at `/admin/`
- [ ] Contact messages appear in admin
- [ ] Messages show name, email, message, and timestamp

---

## Quick Reference: Commands

| Action | Command |
|--------|---------|
| Run Django unit tests | `python manage.py test contact -v 2` |
| Run E2E browser tests | `python tests_e2e.py` |
| Start dev server | `python manage.py runserver` |
| Open Lighthouse | Chrome → F12 → Lighthouse tab |
