from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('/Users/nandolessard/Desktop/Google Chrome.app')

driver.get("https://www.linkedin.com")