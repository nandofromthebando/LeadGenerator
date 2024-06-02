from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
import time

# Click script untested
def execute_javascript_to_click_links(driver, container_selector):
    script = f"""
        function clickAllLinks(containerSelector) {{
            const container = document.querySelector(containerSelector);
            if (container) {{
                const links = container.querySelectorAll('a');
                links.forEach((link, index) => {{
                    setTimeout(() => {{
                        link.click();
                        console.log(`Clicked link ${{index + 1}}: ${{link.href}}`);
                    }}, index * 1000);
                }});
            }} else {{
                console.log('Container not found');
            }}
        }}
        clickAllLinks('{container_selector}');
    """
    driver.execute_script(script)
    
def custom_google_search(query, language="en", region="US"):
    try:
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
        time.sleep(5)  # Allow some time for the page to load

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

        # Scrape all the elements as bot scrolls through
        items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')
        results = []
        for  item in items:
            data = {}

            try:
                data['Company Name'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
            except Exception:
                pass
            
            try:
                data['link'] = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            except Exception:
                pass

            try:
                data['website'] = item.find_element(By.CSS_SELECTOR, "a.A1zNzb").get_attribute('href')
            except Exception:
                pass

            try:
                rating_text = item.find_element(By.CSS_SELECTOR, '.fontBodyMedium > span[role = "img"]').get_attribute('aria-label')
                rating_nums = [float(piece.replace(",", ".")) for piece in rating_text.split(" ") if piece.replace(",", ".").replace(".", "", 1).isdigit()]

                if rating_nums:
                    data['stars'] = rating_nums[0]
                    data['reviews'] = int(rating_nums[1]) if len(rating_nums) > 1 else 0
            except Exception:
                pass

            if (data.get('Company Name')):
                results.append(data)
            
        with open('results.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False,  indent=2)
    finally:
        time.sleep(60)
        driver.quit()

'''query = "medical salons 02301"
custom_google_search(query)'''