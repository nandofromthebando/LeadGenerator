from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def custom_google_search(query, language="en", region="US"):
    # Configure Chrome options to deny geolocation permissions
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-infobars")  # Disable infobars
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    chrome_options.add_argument("--allow-file-access-from-files")  # Allow file access from files
    chrome_options.add_argument("--disable-geolocation")  # Disable geolocation
    
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Construct the Google search URL
    url = f"https://www.google.com/maps/search/?q={'+'.join(query.split())}&hl={language}&gl={region}"

    # Open the Google search page
    driver.get(url)
    time.sleep(3)  # Allow some time for the page to load

    # Scroll down incrementally to load dynamic content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down by 1000 pixels
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)  # Wait for content to load

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # If the height hasn't changed, break the loop
        last_height = new_height

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

    # Collect rows in a list of dictionaries
    rows = []
    for x in range(min_length):
        biz_name = boxes[x].find('div', class_='NrDZNb').text
        num_reviews = boxes[x].find('span', class_='UY7F9', attrs={'aria-hidden': 'true'}).text
        rating = boxes[x].find('span', attrs={'aria-hidden': 'true'}).text
        rows.append({
            'Business name': biz_name,
            'Link to book': links[x],
            'Number of reviews': num_reviews,
            'Rating': rating
        })

    # Convert the list of dictionaries to a DataFrame and concatenate
    new_df = pd.DataFrame(rows)
    df = pd.concat([new_df], ignore_index=True)

    driver.quit()  # Close the browser

    print(df)

# Test usage before adding it to the main
query = "medical salons near 02301"  # Google Search Result
custom_google_search(query)
