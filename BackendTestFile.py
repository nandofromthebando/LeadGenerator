from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
from bs4 import BeautifulSoup
import pandas as pd
import time

def custom_google_search(query, language="en", region="US"):
    # Configure Chrome options to deny geolocation permissions
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--disable-geolocation")

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Construct the Google search URL
    url = f"https://www.google.com/maps/search/?q={'+'.join(query.split())}&hl={language}&gl={region}"

    # Open the Google search page
    driver.get(url)
    time.sleep(3)  # Allow some time for the page to load

    rows = []

    # This is what scrolls through the pages
    scrollable_div = driver.find_element(By.CSS_SELECTOR,'div[role="feed"]' )
    # JavaScript code to be executed
    scroll_script = """
          var scrollableDiv = arguments[0];
          function scrollWithinElement(scrollableDiv) {
              return new Promise((resolve, reject) => {
                  var totalHeight = 0;
                  var distance = 1000;
                  var scrollDelay = 3000;
                  
                  var timer = setInterval(() => {
                      var scrollHeightBefore = scrollableDiv.scrollHeight;
                      scrollableDiv.scrollBy(0, distance);
                      totalHeight += distance;

                      if (totalHeight >= scrollHeightBefore) {
                          totalHeight = 0;
                          setTimeout(() => {
                              var scrollHeightAfter = scrollableDiv.scrollHeight;
                              if (scrollHeightAfter > scrollHeightBefore) {
                                  return;
                              } else {
                                  clearInterval(timer);
                                  resolve();
                              }
                          }, scrollDelay);
                      }
                  }, 200);
              });
          }
          return scrollWithinElement(scrollableDiv);

    """

    # Execute the JavaScript in the context of the scrollable div
    driver.execute_script(scroll_script, scrollable_div)
    try:
        while True:
            # Get the page source after scrolling
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # Find all sub elements
            boxes = soup.find_all('div', class_='Z8fK3b')
            links_to_sites = soup.find_all('a', class_='A1zNzb')

            links = []
            for link in links_to_sites:
                href = link.get('href')
                if href:
                    links.append(href)

            min_length = min(len(boxes), len(links))

            for x in range(min_length):
                try:
                    biz_name_element = boxes[x].find('div', class_='NrDZNb')
                    num_reviews_element = boxes[x].find('span', class_='UY7F9', attrs={'aria-hidden': 'true'})
                    rating_element = boxes[x].find('span', attrs={'aria-hidden': 'true'})

                    # Ensure all elements are found and not None
                    if biz_name_element and num_reviews_element and rating_element:
                        biz_name = biz_name_element.text.strip()
                        num_reviews = num_reviews_element.text.strip()
                        rating = rating_element.text.strip()

                        rows.append({
                            'Business name': biz_name,
                            'Link to book': links[x],
                            'Number of reviews': num_reviews,
                            'Rating': rating
                        })

                except Exception as e:
                    print(f"Error processing box {x}: {e}")
    except Exception as e:
        print(f"Error during search: {e}")
    finally:
        driver.quit()  # Close the browser

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(rows)
    print(df)

# Test usage before adding it to the main
query = "medical salons near ma"
custom_google_search(query)
