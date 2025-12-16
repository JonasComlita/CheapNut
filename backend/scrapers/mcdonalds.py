from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class McDonaldsScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        # McDonald's menu is usually https://www.mcdonalds.com/us/en-us/full-menu.html
        url = "https://www.mcdonalds.com/us/en-us/full-menu.html"
        self.driver.get(url)
        
        results = []
        try:
            # Wait for menu grid
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.cmp-category__item"))
            )
            
            # This logic captures items but McDs usually hides price until location selected or in app.
            # We will scrape names and set price to 0.0 (or estimate/mock later) if not found.
            # Some regions show prices.
            
            items = self.driver.find_elements(By.CSS_SELECTOR, "li.cmp-category__item")
            
            for item in items:
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, ".cmp-category__item-name")
                    name = name_el.text
                    
                    if query.lower() in name.lower():
                        price = 0.0 # Prices often require location/ordering flow
                        
                        img_url = ""
                        try:
                            img_el = item.find_element(By.CSS_SELECTOR, "img")
                            img_url = img_el.get_attribute("src")
                        except:
                            pass

                        results.append({
                            "name": name,
                            "price": price,
                            "unit": "item",
                            "store": "McDonald's",
                            "type": "restaurant",
                            "nutrition": {},
                            "image": img_url
                        })
                except:
                    continue
                    
            return results[:10]
        except Exception as e:
            logging.error(f"Error scraping McDonald's: {e}")
            return []
