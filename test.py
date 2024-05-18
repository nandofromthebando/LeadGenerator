from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

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
    driver = webdriver.Chrome()

    # Construct the Google search URL
    url = f"https://www.google.com/maps/search/?q={'+'.join(query.split())}&hl={language}&gl={region}"

    # Open the Google search page
    driver.get(url)

    # Get the page source after some time for dynamic content to load
    driver.implicitly_wait(10)  # Wait for up to 10 seconds for elements to load
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Find all elements with the specified class
    boxes = soup.find_all('li', class_='hfpxzc')  # Boxes HTML variables, contain profiles of businesses

    # Test if they are there
    print(len(boxes))

'''    while(True):
        pass'''


# Test usage before adding it to the main
query = "medical salons near 02301" # Google Search Result
custom_google_search(query)