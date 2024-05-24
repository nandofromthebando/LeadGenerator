from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

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
    try:
        while True:
            # Get the page source after scrolling
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # Find all sub elements
            boxes = soup.find_all('div', class_='Z8fK3b')
            # Extract information from each box 
            links_to_sites = soup.find_all('a', class_='A1zNzb')

            links = []
            for link in links_to_sites:
                href = link.get('href')
                if href:  # Check if href attribute exists
                    links.append(href)

            # Ensure the number of boxes and links are the same
            min_length = min(len(boxes), len(links))

            for x in range(min_length):
                try:
                    biz_name = boxes[x].find('div', class_='NrDZNb').text
                    num_reviews = boxes[x].find('span', class_='UY7F9', attrs={'aria-hidden': 'true'}).text
                    rating = boxes[x].find('span', attrs={'aria-hidden': 'true'}).text
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
            time.sleep(1)
            
            # Break the loop after some reasonable number of iterations or a condition
            if len(rows) > 50:  # For example, stop after collecting data for 50 businesses
                break

    except Exception as e:
        print(f"Error during search: {e}")
    finally:
        driver.quit()  # Close the browser

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(rows)
    print(df)

# Test usage before adding it to the main
query = "medical salons near 02301"  # Google Search Result
custom_google_search(query)
