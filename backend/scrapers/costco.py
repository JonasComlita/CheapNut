from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class CostcoScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        url = f"https://www.costco.com/CatalogSearch?dept=All&keyword={query}"
        self.driver.get(url)
        
        results = []
        try:
            # Costco usually hides prices for non-members on many items
            # But we can try to scrape what's visible
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-list, .product-tile"))
            )
            
            items = self.driver.find_elements(By.CSS_SELECTOR, ".product-list .product")
            if not items:
                items = self.driver.find_elements(By.CSS_SELECTOR, ".product-tile")
            
            for item in items[:10]:
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, ".description a")
                    name = name_el.text
                    
                    try:
                        price_el = item.find_element(By.CSS_SELECTOR, ".price")
                        price_text = price_el.text.strip().replace('$', '')
                        price = float(price_text)
                    except:
                        price = 0.0 # Login required

                    results.append({
                        "name": name,
                        "price": price,
                        "unit": "bulk",
                        "store": "Costco",
                        "type": "grocery",
                        "nutrition": {}
                    })
                except:
                    continue
            return results
        except Exception as e:
            logging.error(f"Error scraping Costco: {e}")
            return []
