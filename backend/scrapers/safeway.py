from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class SafewayScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        url = f"https://www.safeway.com/shop/search-results.html?q={query}"
        self.driver.get(url)
        
        results = []
        try:
            # Common Safeway selectors
            # Container: product-item-inner-container or data-test-id="product-item-container"
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-card-container, div[data-qa='product-card']"))
            )
            
            items = self.driver.find_elements(By.CSS_SELECTOR, "div.product-card-container, div[data-qa='product-card']")
            
            for item in items[:10]:
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, "a.product-title, [data-qa='product-title']")
                    name = name_el.text
                    
                    try:
                        price_el = item.find_element(By.CSS_SELECTOR, "span.product-price, [data-qa='product-price']")
                        price_text = price_el.text.strip().replace('$', '').split()[0] # Handle "$5.99 / ea"
                        price = float(price_text)
                    except:
                        price = 0.0
                        
                    try:
                        img_el = item.find_element(By.TAG_NAME, "img")
                        img_url = img_el.get_attribute("src")
                    except:
                        img_url = ""

                    results.append({
                        "name": name,
                        "price": price,
                        "unit": "item",
                        "store": "Safeway",
                        "type": "grocery",
                        "nutrition": {},
                        "image": img_url
                    })
                except:
                    continue
                    
            return results
        except Exception as e:
            logging.error(f"Error scraping Safeway: {e}")
            return []
