from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def custom_google_search(query, language="en", region="US"):
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
        driver = webdriver.Chrome(options=chrome_options)

        # Construct the Google search URL
        url = f"https://www.google.com/maps/search/?q={'+'.join(query.split())}&hl={language}&gl={region}"

        # Open the Google search page
        driver.get(url)
        time.sleep(3)  # Allow some time for the page to load

        rows = []

        # This is what scrolls through the pages
        scrollable_div = driver.find_element(By.CSS_SELECTOR,'div[role="feed"]' )
        # JavaScript code to be executed
        scroll_script = """
            var scrollableDiv = arguments[0];
            function scrollWithinElement(scrollableDiv){
                return new Promise((resolve, reject)  => {
                    var totalHeight = 0;
                    var distance = 1000;
                    var scrollDelay = 3000;
                    
                    var timer = setInterval(() => {
                        var scrollHeightBefore = scrollableDiv.scrollHeight;
                        scrollableDiv.scrollBy(0, distance);
                        totalHeight += distance;

                        if (totalHeight >= scrollHeightBefore) { 
                            totalHeight = 0;
                            setTimeout(() => {
                                var scrollHeightAfter = scrollableDiv.scrollHeight;
                                if (scrollHeightAfter > scrollHeightBefore){
                                    return;
                                } else {
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, scrollDelay);
                        }
                    }, 200);
                });
            }
            return scrollWithinElement(scrollableDiv);
        """

        # Execute the JavaScript in the context of the scrollable div
        driver.execute_script(scroll_script, scrollable_div)

        # Scrape all the elements as bot scrolls through
        items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')
        results = []
        for  item in items:
            data = {}

            try:
                data['title'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
            except Exception:
                pass

            if (data.get('title')):
                results.append(data)
            
            with open('results.json', '') as f:
                json.dump(results, f, indent=2)
    finally:
        time.sleep(60)
        driver.quit()
# Test usage before adding it to the main
query = "medical salons near ma"
custom_google_search(query)
