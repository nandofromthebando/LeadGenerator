from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://www.linkedin.com/search/results/people/?keywords=real%20estate%20agents&origin=SWITCH_SEARCH_VERTICAL&searchId=eb6c74ed-da5a-4aec-b51e-aa4ab7f5459e&sid=9cj")

soup = BeautifulSoup(driver.page_source, 'lxml')

boxes = soup.find_all('li',class_ ='reusable-search__result-container')
print(len(boxes))