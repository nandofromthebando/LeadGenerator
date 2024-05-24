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
    scrollable_div = driver.find_element(By.CSS_SELECTOR,'div[jsaction="focus:scrollable.focus; blur:scrollable.blur"]' )
    driver.execute("""
        var scrollablediv = arguments[];
        function scrollWithinElement(scrollablediv){
            return Promise((resolve, reject)  => {
                var totalHeight = 0;
                var distance = 1000;
                var scrollDelay = 3000;
                   
                   var timer = setInterval
              })   
        }
        return scrollWithinElement
                   """)
    try:
        while True:
            # Get the page source after scrolling
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # Find all sub elements
            boxes = soup.find_all('div', class_='Z8fK3b')
            links_to_sites = soup.find_all('a', class_='A1zNzb')

            links = []
            for link in links_to_sites:
                href = link.get('href')
                if href:
                    links.append(href)

            min_length = min(len(boxes), len(links))

            for x in range(min_length):
                try:
                    biz_name_element = boxes[x].find('div', class_='NrDZNb')
                    num_reviews_element = boxes[x].find('span', class_='UY7F9', attrs={'aria-hidden': 'true'})
                    rating_element = boxes[x].find('span', attrs={'aria-hidden': 'true'})

                    # Ensure all elements are found and not None
                    if biz_name_element and num_reviews_element and rating_element:
                        biz_name = biz_name_element.text.strip()
                        num_reviews = num_reviews_element.text.strip()
                        rating = rating_element.text.strip()

                        rows.append({
                            'Business name': biz_name,
                            'Link to book': links[x],
                            'Number of reviews': num_reviews,
                            'Rating': rating
                        })

                except Exception as e:
                    print(f"Error processing box {x}: {e}")

            # Scroll to the bottom of the page
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)  # Allow time for new content to load

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:  # Check if we have reached the bottom
                break
            prev_height = new_height

            if len(rows) >= 50:  # Stop after collecting data for 50 businesses
                break

    except Exception as e:
        print(f"Error during search: {e}")
    finally:
        driver.quit()  # Close the browser

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(rows)
    print(df)

# Test usage before adding it to the main
query = "medical salons near 02301"
custom_google_search(query)
