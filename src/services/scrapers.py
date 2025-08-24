from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import shutil

def scrape_bing_sync(bing_url: str) -> str:
    options = Options()
    
    # Essential headless options for cloud deployment
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Try to find Chrome binary in common locations
    chrome_paths = [
        os.environ.get('CHROME_BIN'),  # Check environment variable first
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/opt/render/project/.chrome/chrome",  # Render-specific path
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        shutil.which("chromium")
    ]
    
    chrome_binary = None
    for path in chrome_paths:
        if path and os.path.exists(path):
            chrome_binary = path
            break
    
    if chrome_binary:
        options.binary_location = chrome_binary
        print(f"Using Chrome binary: {chrome_binary}")
    
    driver = None
    film_title = None
    
    try:
        # Try different service configurations
        service = None
        
        # Method 1: Try ChromeDriverManager first
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e1:
            print(f"ChromeDriverManager failed: {e1}")
            
            # Method 2: Try system chromedriver paths
            chromedriver_paths = [
                os.environ.get('CHROMEDRIVER_PATH'),  # Check environment variable
                "/usr/bin/chromedriver",
                "/usr/local/bin/chromedriver",
                shutil.which("chromedriver")
            ]
            
            for chromedriver_path in chromedriver_paths:
                if chromedriver_path and os.path.exists(chromedriver_path):
                    try:
                        service = Service(chromedriver_path)
                        driver = webdriver.Chrome(service=service, options=options)
                        print(f"Using ChromeDriver: {chromedriver_path}")
                        break
                    except Exception as e2:
                        print(f"Failed with {chromedriver_path}: {e2}")
                        continue
            
            # Method 3: Try without explicit service (let Selenium find it)
            if not driver:
                try:
                    driver = webdriver.Chrome(options=options)
                except Exception as e3:
                    print(f"Default Chrome initialization failed: {e3}")
                    return None
        
        if not driver:
            print("Failed to initialize Chrome WebDriver")
            return None
            
        # Proceed with scraping
        driver.get(bing_url)
        wait = WebDriverWait(driver, 15)

        # Wait for the search box
        search_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.b_searchbox"))
        )

        # Clear and enter search query
        search_box.clear()
        search_box.send_keys("return the film title as a heading")
        search_box.send_keys(Keys.RETURN)

        # Wait for result title
        film_title_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".semi-ew-wrapper .semi-ew h1"))
        )

        film_title = film_title_element.text.strip()
        print(f"Successfully scraped film title: {film_title}")

    except Exception as e:
        print(f"Error during scraping: {e}")
        film_title = None

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")

    return film_title