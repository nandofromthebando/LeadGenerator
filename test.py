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

    # Get the page source after some time for dynamic content to load
    driver.implicitly_wait(10)  # Wait for up to 10 seconds for elements to load
    df = pd.DataFrame(columns=['Business name', 'Link to book', 'Number of reviews', 'Rating'])  # Create a df to store all the information

    # Parse the page source with BeautifulSoup
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

    # Extract information from each box and append to the DataFrame
    for x in range(min_length):
        biz_name = boxes[x].find('div', class_='NrDZNb').text
        num_reviews = boxes[x].find('span', class_='UY7F9', attrs={'aria-hidden': 'true'}).text
        rating = boxes[x].find('span', attrs={'aria-hidden': 'true'}).text
        df = df._append({
            'Business name': biz_name,
            'Link to book': links[x],
            'Number of reviews': num_reviews,
            'Rating': rating
        }, ignore_index =True)

    driver.quit()  # Close the browser

    print(df)

# Test usage before adding it to the main
query = "medical salons near 02301"  # Google Search Result
custom_google_search(query)
