from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class ChipotleScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        url = "https://www.chipotle.com/order"
        self.driver.get(url)
        
        results = []
        try:
            # Chipotle order page
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".entree-item, .item-card"))
            )
            
            items = self.driver.find_elements(By.CSS_SELECTOR, ".entree-item, .item-card")
            
            for item in items:
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, ".item-title, h3")
                    name = name_el.text
                    
                    if query.lower() in name.lower():
                        try:
                            price_el = item.find_element(By.CSS_SELECTOR, ".price")
                            price_text = price_el.text.replace('$', '')
                            price = float(price_text)
                        except:
                            price = 0.0

                        results.append({
                            "name": name,
                            "price": price,
                            "unit": "item",
                            "store": "Chipotle",
                            "type": "restaurant",
                            "nutrition": {}
                        })
                except:
                    continue
            return results[:10]
        except Exception as e:
            logging.error(f"Error scraping Chipotle: {e}")
            return []
