from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def configure_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--disable-geolocation")
    return chrome_options

def search_for_info(query, language="en", region="US"):
    try:
        chrome_options = configure_chrome_options()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        url = f"https://www.google.com/search?q={'+'.join(query.split())}&hl={language}&gl={region}"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))
        time.sleep(5)  # Allow some time for the page to load completely
    finally:
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
    search_for_info(search)
