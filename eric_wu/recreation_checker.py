from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import pytz


# # Production
# USERNAME = ""
# PASSWORD = ""
# TICKET_PAGE_URL = "https://www.recreation.gov/ticket/249985/ticket/10253611"
# TARGET_DATE = "08/29/2025"  # Format: MM/DD/YYYY
# TIME_BLOCK = "8:00 a.m. to 8:59 a.m."  # Desired time block
# NUM_PEOPLE = "4"  # Number of people (up to 4 per ticket)
# RELEASE_TIME = datetime(2025, 8, 22, 8, 0, 0)  # 8:00 AM MDT on Aug 23, 2025


## Test
USERNAME = ""
PASSWORD = ""
TICKET_PAGE_URL = "https://www.recreation.gov/timed-entry/10112683/ticket/10112684"
TARGET_DATE = "08/30/2025"  # Format: MM/DD/YYYY
TIME_BLOCK = "9:00 a.m. to 10:00 a.m."  # Desired time block
NUM_PEOPLE = "4"  # Number of people (up to 4 per ticket)
RELEASE_TIME = datetime(2025, 8, 30, 8, 0, 0)  # 8:00 AM MDT on Aug 23, 2025

# t up timezone for Mountain Daylight Time (MDT)
tz = pytz.timezone('US/Mountain')
RELEASE_TIME = tz.localize(RELEASE_TIME)

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Comment out for testing
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("window-size=1280,800")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(5)

try:
    # Step 1: Navigate to ticket page
    print("Navigating to ticket page...")
    driver.get(TICKET_PAGE_URL)
    print("Page loaded. Title:", driver.title)
    print("Current URL:", driver.current_url)
    driver.save_screenshot("ticket_page.png")

    # Step 2: Click Sign In button
    print("Looking for Sign Up / Log In button...")
    sign_in_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "ga-global-nav-log-in-link"))
    )
    sign_in_button.click()
    print("Clicked Sign Up / Log In button. Current URL:", driver.current_url)
    driver.save_screenshot("post_sign_in_click.png")

    # Step 3: Enter credentials on login page with robust error handling
    print("Waiting for login form...")
    try:
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        print("Email field found.")
        email_field.send_keys(USERNAME)
    except Exception as e:
        print(f"Error finding email field: {e}")
        driver.save_screenshot("error_email_field.png")
        raise

    try:
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        print("Password field found.")
        password_field.send_keys(PASSWORD)
    except Exception as e:
        print(f"Error finding password field: {e}")
        driver.save_screenshot("error_password_field.png")
        raise

    try:
        # Try multiple XPaths for the login button
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'SIGNLOG ', 'signlog '), 'log in') or contains(translate(., 'SIGNLOG ', 'signlog '), 'sign in')]"))
        )
        print("Login button found.")
        login_button.click()
    except Exception as e:
        print(f"Error finding/clicking login button: {e}")
        driver.save_screenshot("error_login_button.png")
        # Try fallback by CSS selector if available
        try:
            login_button_alt = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-submit-btn'], button[type='submit']"))
            )
            print("Login button (alt) found.")
            login_button_alt.click()
        except Exception as e2:
            print(f"Fallback login button also failed: {e2}")
            driver.save_screenshot("error_login_button_alt.png")
            raise

    print("Login attempted. Current URL:", driver.current_url)
    driver.save_screenshot("post_login_attempt.png")

    # Step 5: Wait until release time
    print("Waiting for release time...")
    while datetime.now(tz) < RELEASE_TIME:
        time.sleep(0.01)

    print("Release time reached! Attempting to book...")
    driver.refresh()

    # Step 6: Select date using editable divs
    print("Selecting date...")
    calendar_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.toggle-calendar-button"))
    )
    calendar_button.click()
    time.sleep(0.5)
    month, day, year = TARGET_DATE.split("/")
    month_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='month, ']"))
    )
    month_div.click()
    month_div.send_keys(month)
    day_div = driver.find_element(By.XPATH, "//div[@aria-label='day, ']")
    day_div.click()
    day_div.send_keys(day)
    year_div = driver.find_element(By.XPATH, "//div[@aria-label='year, ']")
    year_div.click()
    year_div.send_keys(year)
    print("Date entered.")
    time.sleep(0.5)

    # Step 7: Set quantity by clicking + button multiple times
    print(f"Setting quantity to {NUM_PEOPLE} tickets...")
    
    # Find the quantity selector area
    quantity_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "10253611"))
    )
    quantity_button.click()
    time.sleep(0.5)
    
    # Click the + button multiple times to reach desired quantity
    try:
        # Look for the + button with aria-label "Add Adults"
        plus_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Add Adults']"))
        )
        
        # Start from 1 and click + button (NUM_PEOPLE - 1) times to reach desired quantity
        current_quantity = 1
        while current_quantity < int(NUM_PEOPLE):
            plus_button.click()
            current_quantity += 1
            time.sleep(0.2)  # Small delay between clicks
            print(f"Clicked + button. Current quantity: {current_quantity}")
        
        print(f"Successfully set quantity to {NUM_PEOPLE} tickets")
    except Exception as e:
        print(f"Could not set quantity using + button: {e}, proceeding with default")

    # Step 8: Click Request Tickets
    print("Clicking Request Tickets...")
    request_tickets_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "request-tickets"))
    )
    request_tickets_button.click()
    print("Request Tickets clicked.")
    driver.save_screenshot("request_tickets_confirmation.png")
    # Switch to interactive mode
    input("Automation complete. You may now interact with the browser manually. Press Enter to exit and close the browser...")
    # Switch to interactive mode
    input("Automation complete. You may now interact with the browser manually. Press Enter to exit and close the browser...")

except Exception as e:
    print(f"Error during automation: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("Screenshot saved as error_screenshot.png")

finally:
    driver.quit()