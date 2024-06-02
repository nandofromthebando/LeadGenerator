from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
import time



def search_for_info(query, language="en", region="US"):
    try:
        # Configure Chrome options to deny geolocation permissions
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--allow-file-access-from-files")
        chrome_options.add_argument("--disable-geolocation")

        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Construct the Google search URL
        url = f"https://www.google.com/search?q={'+'.join(query.split())}&hl={language}&gl={region}"

        # Open the Google search page
        driver.get(url)
        time.sleep(5)  # Allow some time for the page to load

    finally:
        driver.quit()

query = "test business"
search_for_info(query)