from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def scrape_bing_sync(bing_url: str) -> str:
    edge_options = EdgeOptions()
    edge_options.add_argument("--headless")  # run without opening window
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    # edge_options.add_argument("--disable-gpu")
    # edge_options.add_argument("--disable-blink-features=AutomationControlled")
    # edge_options.add_argument("--blink-settings=imagesEnabled=false")

    service = EdgeService(r"C:\Drivers\msedgedriver.exe")

    driver = webdriver.Edge(service=service, options=edge_options)
      
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
        film_title_element = WebDriverWait(driver, 20).until(
         EC.presence_of_element_located((By.CSS_SELECTOR, ".semi-ew-wrapper .semi-ew h1"))
        )

        film_title = film_title_element.text.strip()

    except Exception as e:
        film_title = None

    # finally:
    #     driver.quit()

    return film_title