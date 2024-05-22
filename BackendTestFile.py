from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


# Path to Chrome binary
chrome_binary = '/Users/underwater56/Downloads/chromedriver-mac-arm64/chromedriver'

# Set Chrome service
chrome_service = ChromeService(chrome_binary)

# Set Chrome options
chrome_options = webdriver.ChromeOptions()

# Pass Chrome service and options to Chrome WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
time.sleep(10) 
# Maximize browser window
driver.maximize_window()

# LinkedIn login URL
url = "https://www.linkedin.com/login"
# Flag variable to control the loop
running = True

# Loop until user stops it
while running:
    # Add a delay to keep the browser window open for inspection
    time.sleep(10)  # Adjust the delay as needed (in seconds)

    # Check if the user wants to stop the loop
    user_input = input("Press 's' to stop the loop: ")
    if user_input.lower() == 's':
        running = False

    else:
        time.sleep(5)
        # Navigate to LinkedIn login page
        driver.get(url)
        time.sleep(3)
        df = pd.DataFrame({'Link':[''], 'Name':[''], 'Job Title':[''], 'Location':['']})  # Create a df to store all the information

        while True:
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # Find all elements with the specified class
            boxes = soup.find_all('li', class_='reusable-search__result-container')  # Boxes HTML variables, contain profiles
            # Extract information from each box (example)
            for i in boxes:
                try:
                    link = i.find('a').get('href') # Href holds links in html
                    name = i.find('span', {'dir','ltr'}).find('span',{'app-aware-link':'true'})  
                    title = i.find('div',class_ = 'entity-result__primary-subtitle t-14 t-black t-normal').text
                    location = i.find('div',class_ = 'entity-result__secondary-subtitle t-14 t-normal').text
                    # Adds name, title, location and link to the dataframe
                    df.append(({'Link':link, 'Name':name, 'Job Title':title, 'Location':location}),ignore_index =True)
                except:
                    pass
            # For scrolling to the bottom of the page
            driver.execute_script('window.scrollTo(0,document.body.scroll Hieght)')
            time.sleep(1)

            # For clicking through the pages pg 2 and so on (skip page 1 different html)
            driver.find_elemnt_by_xpath('/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[4]/div/div/button[2]').click()
            time.sleep(3)

