import time
import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:8000"


def setup_driver():
    """Initialize Chrome in headed mode so you can watch the tests."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    return driver


def test_homepage_loads(driver):
    """Test 1: Homepage loads and shows the correct title."""
    driver.get(BASE_URL)
    assert "RAGHAVARAJAN" in driver.title, f"Expected 'RAGHAVARAJAN' in title, got: {driver.title}"
    print("[PASS] Test 1: Homepage loads with correct title")


def test_navigation_links(driver):
    """Test 2: All nav links exist and scroll to sections."""
    driver.get(BASE_URL)
    sections = ["about", "skills", "projects", "education", "contact"]
    for section in sections:
        link = driver.find_element(By.CSS_SELECTOR, f'a[href="#{section}"]')
        assert link is not None, f"Nav link for #{section} not found"
    print("[PASS] Test 2: All navigation links present")


def test_sections_exist(driver):
    """Test 3: All main sections are present on the page."""
    driver.get(BASE_URL)
    for section_id in ["hero", "about", "skills", "projects", "education", "contact"]:
        section = driver.find_element(By.ID, section_id)
        assert section is not None, f"Section #{section_id} not found"
    print("[PASS] Test 3: All sections exist on the page")


def test_contact_form_success(driver):
    """Test 4: Contact form submits successfully and shows green alert."""
    driver.get(BASE_URL + "/#contact")
    time.sleep(1)

    driver.find_element(By.ID, "contact-name").send_keys("Selenium Test")
    driver.find_element(By.ID, "contact-email").send_keys("selenium@test.com")
    driver.find_element(By.ID, "contact-message").send_keys("Automated test message")

    driver.find_element(By.ID, "contact-submit-btn").click()
    time.sleep(2)

    alert = driver.find_element(By.ID, "form-alert")
    assert alert.is_displayed(), "Alert banner did not appear"
    alert_text = driver.find_element(By.ID, "form-alert-text").text
    assert "success" in alert_text.lower(), f"Expected success message, got: {alert_text}"
    print("[PASS] Test 4: Contact form submits and shows success alert")


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
    print("[PASS] Test 5: Form fields clear after successful submission")


def test_responsive_mobile(driver):
    """Test 6: Site renders properly at mobile width."""
    driver.set_window_size(375, 812)
    driver.get(BASE_URL)
    time.sleep(1)

    body = driver.find_element(By.TAG_NAME, "body")
    assert body.size['width'] <= 375, "Page is wider than mobile viewport"
    print("[PASS] Test 6: Site fits mobile viewport")
    driver.set_window_size(1400, 900)


def test_admin_login(driver):
    """Test 7: Django admin panel is accessible and login works."""
    driver.get(BASE_URL + "/admin/")
    time.sleep(1)

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    time.sleep(2)

    assert "Site administration" in driver.page_source, "Admin login failed"
    print("[PASS] Test 7: Admin login works")


def test_messages_in_admin(driver):
    """Test 8: Submitted messages appear in admin panel."""
    driver.get(BASE_URL + "/#contact")
    time.sleep(1)
    driver.find_element(By.ID, "contact-name").send_keys("Admin Check")
    driver.find_element(By.ID, "contact-email").send_keys("admin@check.com")
    driver.find_element(By.ID, "contact-message").send_keys("Verify in admin")
    driver.find_element(By.ID, "contact-submit-btn").click()
    time.sleep(2)

    driver.get(BASE_URL + "/admin/contact/contactmessage/")
    time.sleep(1)

    if "login" in driver.current_url:
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        time.sleep(2)

    assert "Admin Check" in driver.page_source, "Submitted message not found in admin"
    print("[PASS] Test 8: Messages visible in admin panel")


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
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print(f"{'='*50}")

    driver.quit()
