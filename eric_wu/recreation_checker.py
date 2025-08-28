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
from credentials import USERNAME, PASSWORD

# TARGET URL
TICKET_PAGE_URL = "https://www.recreation.gov/timed-entry/10087086/ticket/10087087"
TARGET_DATE = "08/30/2025"  # Format: MM/DD/YYYY
NUM_PEOPLE = "1"  # Number of people (up to 4 per ticket)
TIME_BLOCK = "7:00 AM - 9:00 AM"
RELEASE_TIME = datetime(2025, 8, 29, 19, 0, 0)  # 8:00 AM MDT on Aug 23, 2025

# TICKET_PAGE_URL = "https://www.recreation.gov/timed-entry/10112683/ticket/10112684"
# TARGET_DATE = "08/30/2025"  # Format: MM/DD/YYYY
# NUM_PEOPLE = "4"  # Number of people (up to 4 per ticket)
# TIME_BLOCK = "7:00 AM - 8:00 AM"
# TIME_BLOCK = "8:00 AM - 9:00 AM"
# TIME_BLOCK = "9:00 AM - 10:00 AM"
# TIME_BLOCK = "10:00 AM - 11:00 AM"
# RELEASE_TIME = datetime(2025, 8, 23, 8, 0, 0)  # 8:00 AM MDT on Aug 23, 2025

# TEST CASE
# TICKET_PAGE_URL = "https://www.recreation.gov/ticket/249985/ticket/10253611"
# TICKET_PAGE_URL = "https://www.recreation.gov/timed-entry/10112471/ticket/10112472"
# TICKET_PAGE_URL = "https://www.recreation.gov/ticket/251610/ticket/182"
# TICKET_PAGE_URL  = "https://www.recreation.gov/timed-entry/10088426/ticket/10088427"
# TICKET_PAGE_URL = "https://www.recreation.gov/ticket/10088514/ticket/10088517"
# TICKET_PAGE_URL = "https://www.recreation.gov/ticket/10101955/ticket/10101956"
# TARGET_DATE = "09/13/2025"  # Format: MM/DD/YYYY
# TIME_BLOCK = "4:30"  # Desired time block
# NUM_PEOPLE = "3"  # Number of people (up to 4 per ticket)
# RELEASE_TIME = datetime(2025, 8, 23, 1, 51, 0)  # 8:00 AM MDT on Aug 23, 2025

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
        # Try multiple selectors for the login button
        try:
            # Try by button text using XPath
            login_button = driver.find_element(By.XPATH, "//button[@type='submit' and .//span[contains(text(), 'Log In')]]")
            print("Login button found by XPath.")
            login_button.click()
        except Exception as e:
            print(f"Error finding/clicking login button by XPath: {e}")
            driver.save_screenshot("error_login_button.png")
            # Try fallback by CSS selector if available
            try:
                login_button_alt = driver.find_element(By.CSS_SELECTOR, "button.rec-acct-sign-in-btn, button[type='submit']")
                print("Login button (alt) found by CSS selector.")
                login_button_alt.click()
            except Exception as e2:
                print(f"Fallback login button also failed: {e2}")
                driver.save_screenshot("error_login_button_alt.png")
                raise
    except Exception as e:
        print(f"Error during login button process: {e}")
        driver.save_screenshot("error_login_button_process.png")
        raise

    time.sleep(0.5) # wait for login to complete

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
    calendar_button = driver.find_element(By.CSS_SELECTOR, "button.toggle-calendar-button")
    calendar_button.click()
    time.sleep(0.5)
    month, day, year = TARGET_DATE.split("/")
    month_div = driver.find_element(By.XPATH, "//div[@aria-label='month, ']")
    month_div.click()
    month_div.send_keys(month)
    day_div = driver.find_element(By.XPATH, "//div[@aria-label='day, ']")
    day_div.click()
    day_div.send_keys(day)
    year_div = driver.find_element(By.XPATH, "//div[@aria-label='year, ']")
    year_div.click()
    year_div.send_keys(year)
    print("Date entered.")
    time.sleep(0.1)

    # Step 7: Compact and readable quantity selection for first ticket type
    print(f"Setting quantity to {NUM_PEOPLE} tickets...")
    quantity_set = False
    try:
        dropdown_btns = driver.find_elements(By.CSS_SELECTOR, "button.rec-select")
        if not dropdown_btns:
            dropdown_btns = driver.find_elements(By.XPATH, "//button[contains(@id, 'guest-counter') or contains(@id, '10253611')]")
        for dropdown_btn in dropdown_btns:
            dropdown_btn.click()
            print("Dropdown quantity selector opened.")
            guest_rows = driver.find_elements(By.CSS_SELECTOR, ".rec-guest-counter-row")
            if guest_rows:
                row = guest_rows[0]
                try:
                    ticket_type = row.find_element(By.CSS_SELECTOR, ".rec-guest-counter-row-title").text.strip()
                    input_field = next((f for f in row.find_elements(By.CSS_SELECTOR, "input.sarsa-text-field-input") if ticket_type.replace(' ', '') in f.get_attribute('id').replace('-', '').replace(' ', '')), None)
                    if not input_field:
                        input_field = row.find_elements(By.CSS_SELECTOR, "input.sarsa-text-field-input")[0]
                    add_btn = row.find_element(By.XPATH, f".//button[contains(@aria-label, 'Add')]")
                    current_quantity = int(input_field.get_attribute("value"))
                    while current_quantity < int(NUM_PEOPLE):
                        if not add_btn.is_enabled():
                            print(f"Add button for {ticket_type} is disabled. Maximum quantity reached or cannot increment further.")
                            break
                        add_btn.click()
                        time.sleep(0.1)
                        current_quantity = int(input_field.get_attribute("value"))
                        print(f"Clicked Add {ticket_type}. Current quantity: {current_quantity}")
                    print(f"Successfully set quantity to {NUM_PEOPLE} for {ticket_type}.")
                    quantity_set = True
                except Exception:
                    pass
            # Close dropdown with ESC
            from selenium.webdriver.common.keys import Keys
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1)
            print("Sent ESC key to close dropdown.")
    except Exception as e:
        print(f"Quantity selection failed: {e}")
    if not quantity_set:
        print("Could not set any ticket quantity.")

    import time as _time
    # Step 8: Fast and generalized timeblock selection with profiling
    print(f"Selecting timeblock: {TIME_BLOCK}")
    try:
        start_labels = _time.time()
        timeblock_labels = driver.find_elements(By.XPATH, "//label[@data-component='RadioPill']")
        end_labels = _time.time()
        print(f"Time to find timeblock labels: {end_labels - start_labels:.4f} seconds")
        found = False
        start_find = _time.time()
        for label in timeblock_labels:
            try:
                # Find the time text in any descendant with *-radio-pill-time class
                time_divs = label.find_elements(By.XPATH, ".//*[contains(@class, '-radio-pill-time')]")
                time_text = None
                for div in time_divs:
                    txt = div.text.strip()
                    if txt:
                        time_text = txt
                        break
                # Fallback: look for recognizable time text in label
                if not time_text:
                    possible_texts = label.text.split('\n')
                    for t in possible_texts:
                        if any(x in t for x in [":", "AM", "PM"]):
                            time_text = t.strip()
                            break
                # Print the time block found
                if time_text:
                    print(f"Found time block: {time_text}")
                # Only select enabled timeblocks
                input_elem = label.find_element(By.TAG_NAME, "input")
                is_enabled = input_elem.is_enabled()
                if time_text and TIME_BLOCK in time_text and is_enabled:
                    label.click()
                    print(f"Selected timeblock: {time_text}")
                    found = True
                    break
            except Exception as e:
                pass  # Silently skip labels that cannot be read
        end_find = _time.time()
        print(f"Time to find and select timeblock: {end_find - start_find:.4f} seconds")
        if not found:
            print(f"Could not find enabled timeblock matching: {TIME_BLOCK}")
    except Exception as e:
        print(f"Error selecting timeblock: {e}")

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

except Exception as e:
    print(f"Error during automation: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("Screenshot saved as error_screenshot.png")

finally:
    driver.quit()