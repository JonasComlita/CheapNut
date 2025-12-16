from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class TraderJoesScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        url = f"https://www.traderjoes.com/home/search?q={query}"
        self.driver.get(url)
        
        results = []
        try:
            # Trader Joes has a nice clean React site usually
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article.SearchResultCard_searchResultCard__3V-_h"))
            )
            # Fallback if class names change (they look generated)
            # Try finding by semantic structure if possible or data attribute
            
            items = self.driver.find_elements(By.CSS_SELECTOR, "article[data-testid='search-result-card'], article")
            
            for item in items[:10]:
                try:
                    name_el = item.find_element(By.CSS_SELECTOR, "h3.SearchResultCard_searchResultCard__title__32e8_ a, h3 a")
                    name = name_el.text
                    
                    try:
                        price_el = item.find_element(By.CSS_SELECTOR, ".ProductPrice_productPrice__price__3-50j, .price")
                        price_text = price_el.text.strip().replace('$', '')
                        price = float(price_text)
                    except:
                        price = 0.0

                    results.append({
                        "name": name,
                        "price": price,
                        "unit": "item", 
                        "store": "Trader Joe's",
                        "type": "grocery",
                        "nutrition": {}
                    })
                except:
                    continue
            return results
        except Exception as e:
            logging.error(f"Error scraping Trader Joe's: {e}")
            return []
