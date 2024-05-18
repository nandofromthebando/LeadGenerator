from selenium import webdriver
from bs4 import BeautifulSoup

def custom_google_search(query, language="en", region="US"):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    # Construct the Google search URL
    url = f"https://www.google.com/search?q={'+'.join(query.split())}&hl={language}&gl={region}"

    # Open the Google search page
    driver.get(url)

    # Get the page source after some time for dynamic content to load
    driver.implicitly_wait(10)  # Wait for up to 10 seconds for elements to load
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML source using Beautiful Soup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all the search result titles using the appropriate CSS selector
    search_results = soup.select("div.dbg0pd span")

    # Print the titles of the search results
    for result in search_results:
        print(result.get_text())

# Example usage
query = "medical salons near 02301"
custom_google_search(query)
