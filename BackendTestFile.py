from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://www.linkedin.com/search/results/people/?keywords=real%20estate%20agents&origin=SWITCH_SEARCH_VERTICAL&searchId=eb6c74ed-da5a-4aec-b51e-aa4ab7f5459e&sid=9cj")

soup = BeautifulSoup(driver.page_source, 'lxml')

# How to bypass logging in, enter credentials

# Enter crendtials func
# Note will have to add to ui place to input crednetials (add fucn to GuiFeatures)
user = input('Username:')   
pw = input('Pawssword:')   
def enter_creds(user, pw):
    # Create a way to log in  with user input ofc
    pass


boxes = soup.find_all('li',class_ ='reusable-search__result-container')   # Boxes HTML variables, contain profiles

print(len(boxes))