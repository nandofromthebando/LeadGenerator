from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

'''# Initialize WebDriver with specified options and chromedriver path
driver = webdriver.Chrome('/opt/homebrew/Caskroom/chromedriver/125.0.6422.60/chromedriver-mac-arm64/chromedriver')

# Open the target URL
driver.get('www.linkedin.com')  # Replace with the actual URL
'''

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')

# Find all elements with the specified class
boxes = soup.find_all('li', class_='reusable-search__result-container')  # Boxes HTML variables, contain profiles

# Print the number of elements found
print(len(boxes))

# Extract information from each box (example)
for i in boxes:
    link = i.find('a').get('href')
    # Assuming there's a name field in the HTML structure
    name = i.find('span', {'dir','ltr'}).find('span',{'app-aware-link':'true'})  
    
    print(f'Name: {name.text if name else "N/A"}, Link: {link}')
    break  # Remove this break if you want to process all boxes
