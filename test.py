#Test file to test different parts of the code
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

# Path to Chrome binary
chrome_binary = '/Users/underwater56/Downloads/chromedriver-mac-arm64/chromedriver'

# Set Chrome service
chrome_service = ChromeService(chrome_binary)

# Set Chrome options
chrome_options = webdriver.ChromeOptions()

# Pass Chrome service and options to Chrome WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Maximize browser window
driver.maximize_window()

# LinkedIn login URL
url = "https://www.linkedin.com/login"

# Navigate to LinkedIn login page
driver.get(url)

time.sleep(10)  # Adjust the delay as needed (in seconds)
