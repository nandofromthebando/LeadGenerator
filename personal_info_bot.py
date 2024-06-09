from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time


def search_for_info(query, language="en", region="US"):
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--allow-file-access-from-files")
        chrome_options.add_argument("--disable-geolocation")
        chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 2
        })
        driver = webdriver.Chrome(options=chrome_options)
        
        # Construct the Google search URL
        url = f"https://www.google.com/search?q={'+'.join(query.split())}&hl={language}&gl={region}"
        driver.get(url)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

        # Click not now for geolocation
        try:
            driver.find_element((By.XPATH, '/html/body/div[5]/div/div[8]/div/div[2]/span/div/div[2]/div[3]/g-raised-button')).click()
        except Exception as e:
            print(f"Location request pop-up did not appear or there was an error: {e}")
   
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

        # Wait for search results to load
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id='search']//a/h3/.."))
        )

        # Loop through search results and click on the first matching result
        target_domain = "openai.com"  # Change this to your target domain
        for result in search_results:
            url = result.get_attribute("href")
            if target_domain in url:
                result.click()
                break
        
        # Wait for the new page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Additional time to let the user see the opened page (can be adjusted or removed as needed)
        time.sleep(5)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def search_json_query(file_path, category):
    json_query = read_json_file(file_path)
    if category not in ["Company Name", "reviews", "stars"]:
        raise ValueError(f"Invalid category '{category}'. Must be one of 'Company Name', 'reviews', or 'stars'.")
    
    return [shop[category] for shop in json_query if category in shop]

# Path to the JSON file
file_path = 'results.json'

# Read search queries from JSON and perform searches
data_search = search_json_query(file_path, 'Company Name')
for search in data_search:
    query = f"{search} founder"
    search_for_info(query)
