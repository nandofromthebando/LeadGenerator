from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

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
                    var scrollDelay = 1000;
                    
                    var timer = setInterval(() => {
                        var scrollHeightBefore = scrollableDiv.scrollHeight;
                        var scrollTopBefore = scrollableDiv.scrollTop;
                        scrollableDiv.scrollBy(0, distance);
                        totalHeight += distance;

                        setTimeout(() => {
                            var scrollHeightAfter = scrollableDiv.scrollHeight;
                            var scrollTopAfter = scrollableDiv.scrollTop;

                            // Check if the scroll height or scroll top has not increased
                            if (scrollTopAfter >= scrollHeightAfter - scrollableDiv.clientHeight || scrollTopAfter === scrollTopBefore) {
                                clearInterval(timer);
                                resolve();
                            }
                        }, scrollDelay);
                    }, scrollDelay);
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

            try:
                text_content = item.text
                phone_pattern = r'((//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[3]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[1]/span[2]/span[2]))'
                matches = re.findall(phone_pattern, text_content)

                phone_numbers = [match[0] for match in matches]
                unique_phone_numbers = list(set(phone_numbers))

                data['address'] = unique_phone_numbers[0] if unique_phone_numbers else None   
            except Exception:
                pass

            if (data.get('Company Name')):
                results.append(data)
            
        with open('results.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False,  indent=2)
    finally:
        time.sleep(60)
        driver.quit()

query = "medical salons ma"
custom_google_search(query)

