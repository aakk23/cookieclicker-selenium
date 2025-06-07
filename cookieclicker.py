from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    logger.info("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Additional webdriver masking
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
    
    logger.info("Navigating to cookieclicker...")
    driver.get('https://orteil.dashnet.org/cookieclicker/')

    # Simulate human-like behavior
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    # Wait for the page to load completely
    WebDriverWait(driver, 30).until(  # Increased timeout
        EC.presence_of_element_located((By.ID, 'langSelect-EN'))
    )
    logger.info("Page loaded successfully.")
    time.sleep(7)  # Increased initial wait
    language_button = driver.find_element(By.ID, 'langSelect-EN')
    time.sleep(5)  # Short wait before clicking the language button
    logger.info("Clicking the language button...")
    language_button.click()

    # Add longer wait after language selection
    time.sleep(3)

    # Check for Cloudflare verification
    logger.info("Checking for Cloudflare verification...")
    try:
        # Wait for Cloudflare iframe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkbox"))
        )
        logger.info("Cloudflare verification detected. Waiting for manual completion...")
        
        # Wait for verification to complete (iframe to disappear)
        WebDriverWait(driver, 60).until_not(
            EC.presence_of_element_located((By.ID, "checkbox"))
        )
        logger.info("Cloudflare verification completed.")
        time.sleep(2)  # Additional wait after verification
    except Exception as e:
        logger.info("No Cloudflare verification found, continuing...")


    # Check if game loaded properly
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'bigCookie'))
        )
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'cookies'))
        )
    except Exception as e:
        logger.error("Game elements not found. Possible bot detection.")
        raise Exception("Bot detection triggered")

    def safe_click_cookie():
        try:
            # Re-find the cookie element each time to avoid stale references
            cookie = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'bigCookie'))
            )
            cookie.click()
            return True
        except Exception as e:
            logger.warning(f"Failed to click cookie: {e}")
            return False

    logger.info("Starting cookie clicking session...")
    successful_clicks = 0
    for i in range(100):
        if safe_click_cookie():
            successful_clicks += 1
        time.sleep(0.2)  # Slightly longer delay between clicks
    
    logger.info(f"Completed clicking session. Successful clicks: {successful_clicks}")
    logger.info("Waiting for 10 seconds to observe the results...")
    
    time.sleep(10)
except Exception as e:
    logger.error(f"An error occurred: {e}")
finally:
    if 'driver' in locals():
        driver.quit()
