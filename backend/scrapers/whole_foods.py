from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class WholeFoodsScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        # Whole Foods via Amazon or their own site (often redirects to Amazon)
        # We'll try the dedicated WF market site if available, or Amazon search
        url = f"https://www.wholefoodsmarket.com/search?text={query}"
        self.driver.get(url)
        
        results = []
        try:
            # Whole Foods often uses wfm-search-result-item
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='product-tile']"))
            )
            
            items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-tile']")
            
            for item in items[:10]:
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, "[data-testid='product-tile-name']")
                    name = name_el.text
                    
                    try:
                        price_el = item.find_element(By.CSS_SELECTOR, ".regular_price, .sale_price")
                        price_text = price_el.text.replace('$', '')
                        price = float(price_text)
                    except:
                        price = 0.0

                    results.append({
                        "name": name,
                        "price": price,
                        "unit": "item",
                        "store": "Whole Foods",
                        "type": "grocery",
                        "nutrition": {}
                    })
                except:
                    continue
            return results
        except Exception as e:
            logging.error(f"Error scraping Whole Foods: {e}")
            return []
