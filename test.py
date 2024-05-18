#Test file to test different parts of the code

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# Set Chrome options
chrome_options = Options()

# Pass Chrome options to Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Maximize browser window
driver.maximize_window()

# LinkedIn login URL
url = "https://www.linkedin.com/login"

# Navigate to LinkedIn login page
driver.get(url)


