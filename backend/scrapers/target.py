from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class TargetScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        url = f"https://www.target.com/s?searchTerm={query}"
        self.driver.get(url)
        
        results = []
        try:
            # Target uses deeply nested React apps. 
            # Look for div[data-test='product-card']
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='product-card']"))
            )
            
            items = self.driver.find_elements(By.CSS_SELECTOR, "[data-test='product-card']")
            
            for item in items[:10]:
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, "[data-test='product-title']")
                    name = name_el.text
                    
                    try:
                        price_el = item.find_element(By.CSS_SELECTOR, "[data-test='current-price']")
                        price_text = price_el.text.strip().replace('$', '')
                        price = float(price_text)
                    except:
                        price = 0.0

                    results.append({
                        "name": name,
                        "price": price,
                        "unit": "item",
                        "store": "Target",
                        "type": "grocery",
                        "nutrition": {}
                    })
                except:
                    continue
            return results
        except Exception as e:
            logging.error(f"Error scraping Target: {e}")
            return []
