from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")  # Start with the browser maximized

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# LinkedIn login URL
url = "https://www.linkedin.com"

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')

# Find all elements with the specified class
boxes = soup.find_all('li', class_='reusable-search__result-container')  # Boxes HTML variables, contain profiles

# Print the number of elements found
print(len(boxes))

df = pd.DataFrame({'Link':[''], 'Name':[''], 'Job Title':[''], 'Location':['']})  # Create a df to store all the information

while True:
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Find all elements with the specified class
    boxes = soup.find_all('li', class_='reusable-search__result-container')  # Boxes HTML variables, contain profiles
    # Extract information from each box (example)
    for i in boxes:
        try:
            link = i.find('a').get('href')
            # Assuming there's a name field in the HTML structure
            name = i.find('span', {'dir','ltr'}).find('span',{'app-aware-link':'true'})  
            title = i.find('div',class_ = 'entity-result__primary-subtitle t-14 t-black t-normal').text
            location = i.find('div',class_ = 'entity-result__secondary-subtitle t-14 t-normal').text
            df.append(({'Link':link, 'Name':name, 'Job Title':title, 'Location':location}))
        except:
            pass
    # For scrolling to the bottom of the page
    driver.execute_script('window.scrollTo(0,document.body.scroll Hieght)')
    time.sleep(1)

    # For clicking through the pages pg 2 and so on (skip page 1 different html)
    driver.find_elemnt_by_xpath('/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[4]/div/div/button[2]').click()
    time.sleep(3)

