from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class WalmartScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        url = f"https://www.walmart.com/search?q={query}"
        self.driver.get(url)
        
        # Check for CAPTCHA
        if "Robot or human?" in self.driver.title:
            logging.warning("Walmart CAPTCHA detected. Manual intervention or stealth driver required.")
            # For now, we return empty, or we could try to wait
            return []

        try:
            # Wait for items to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-item-id]"))
            )
            
            items = self.driver.find_elements(By.CSS_SELECTOR, "div[data-item-id]")
            results = []
            
            for item in items[:10]: # Limit to top 10
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, "span[data-automation-id='product-title']")
                    name = name_el.text
                    
                    try:
                        price_el = item.find_element(By.CSS_SELECTOR, "div[data-automation-id='product-price']")
                        # Price text usually like "$5.16" or "$5.16\ncurrent price"
                        price_text = price_el.text.split('\n')[0].replace('$', '')
                        price = float(price_text)
                    except:
                        price = 0.0

                    try:
                        img_el = item.find_element(By.CSS_SELECTOR, "img[data-testid='productTileImage']")
                        img_url = img_el.get_attribute("src")
                    except:
                        img_url = ""

                    results.append({
                        "name": name,
                        "price": price,
                        "unit": "item", # improved unit parsing needed
                        "store": "Walmart",
                        "type": "grocery",
                        "nutrition": {}, # scraping nutrition details requires clicking into item
                        "image": img_url
                    })
                except Exception as e:
                    logging.warning(f"Error parsing item: {e}")
                    continue
            
            return results
            
        except Exception as e:
            logging.error(f"Error scraping Walmart: {e}")
            return []
