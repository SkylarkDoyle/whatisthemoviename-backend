from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def scrape_bing_sync(bing_url: str) -> str:
    options = Options()
    options.add_argument("--headless")  # run without opening window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--blink-settings=imagesEnabled=false")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
      
    # driver.get(bing_url)

    # wait until element appears
    # driver.implicitly_wait(10)  # seconds

    try:
        driver.get(bing_url)

        wait = WebDriverWait(driver, 15)

        # ✅ 1. Wait for the search box ("Add to your search")
        search_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.b_searchbox"))
        )

        # ✅ 2. Clear any pre-filled imgurl value and type your follow-up query
        search_box.clear()
        search_box.send_keys("return the film title as a heading")
        search_box.send_keys(Keys.RETURN)

        # ✅ 3. Wait for result title to appear
        film_title_element = WebDriverWait(driver, 30).until(
         EC.presence_of_element_located((By.CSS_SELECTOR, ".semi-ew-wrapper .semi-ew h1"))
        )

        film_title = film_title_element.text.strip()

    except Exception as e:
        film_title = None

    # finally:
    #     driver.quit()

    return film_title