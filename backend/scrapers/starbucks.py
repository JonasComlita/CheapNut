from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class StarbucksScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        url = "https://www.starbucks.com/menu"
        self.driver.get(url)
        
        results = []
        try:
            # Starbucks menu is well structured but prices usually require store selection
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='menu-item']"))
            )
            
            items = self.driver.find_elements(By.CSS_SELECTOR, "[data-e2e='menu-item']")
            
            for item in items:
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, "span.block")
                    name = name_el.text
                    
                    if query.lower() in name.lower():
                        price = 0.0 # Hidden until store selected
                        
                        results.append({
                            "name": name,
                            "price": price,
                            "unit": "item",
                            "store": "Starbucks",
                            "type": "restaurant",
                            "nutrition": {}
                        })
                except:
                    continue
            return results[:10]
        except Exception as e:
            logging.error(f"Error scraping Starbucks: {e}")
            return []
