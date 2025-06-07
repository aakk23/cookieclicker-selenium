import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging
product_prefix = 'product'
product_price_prefix = 'productPrice'
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def random_sleep(a=0.5, b=1.5):
    time.sleep(random.uniform(a, b))

def slow_scroll(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    random_sleep(0.5, 1.2)
    driver.execute_script("window.scrollTo(0, 0);")
    random_sleep(0.5, 1.5)

def safe_click_cookie(driver):
    try:
        cookie = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'bigCookie'))
        )
        cookie.click()
        return True
    except Exception as e:
        logger.warning(f"Failed to click cookie: {e}")
        return False

try:
    # Setup Chrome options
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    logger.info("Initializing undetected Chrome WebDriver...")
    driver = uc.Chrome(options=options, headless=False)

    logger.info("Navigating to Cookie Clicker...")
    driver.get('https://orteil.dashnet.org/cookieclicker/')
    random_sleep(2, 4)

    slow_scroll(driver)

    # Wait for language selection
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'langSelect-EN'))
    )
    logger.info("Page loaded. Selecting language...")
    random_sleep()
    driver.find_element(By.ID, 'langSelect-EN').click()

    # Wait after language change
    random_sleep(3, 5)

    # Check for Cloudflare challenge (optional)
    logger.info("Checking for Cloudflare verification...")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkbox"))
        )
        logger.info("Cloudflare challenge found. Waiting for it to clear...")
        WebDriverWait(driver, 60).until_not(
            EC.presence_of_element_located((By.ID, "checkbox"))
        )
        logger.info("Cloudflare challenge passed.")
    except Exception:
        logger.info("No Cloudflare challenge detected.")

    # Wait for game to load
    logger.info("Waiting for main game elements...")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'bigCookie'))
    )
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'cookies'))
    )
    logger.info("Game loaded. Starting clicking session...")

    
    cookie = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'bigCookie'))
    )
    cookie = driver.find_element(By.ID, 'bigCookie')
    while True:
        try:
            cookie.click()
            cookies_text = driver.find_element(By.ID, 'cookies').text.split(" ")[0]
            cookies_count = int(cookies_text.replace(',', ''))
            
            for i in range(4):
                try:
                    product_price_elem = driver.find_element(By.ID, product_price_prefix + str(i))
                    if not product_price_elem.text:
                        continue
                    product_price = int(product_price_elem.text.replace(',', ''))
                    
                    if cookies_count >= product_price:
                        product = driver.find_element(By.ID, product_prefix + str(i))
                        product.click()
                        break
                except (ValueError, Exception) as e:
                    logger.debug(f"Error processing product {i}: {e}")
                    continue
                    
        except Exception as e:
            logger.warning(f"Error in main loop: {e}")
            continue

    logger.info("Waiting to observe game for 10 seconds...")
    time.sleep(10)

except Exception as e:
    logger.error(f"An error occurred: {e}")
