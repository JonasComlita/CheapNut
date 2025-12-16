from .base_selenium import SeleniumScraper
from .interface import ProductInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class JackInTheBoxScraper(SeleniumScraper):
    def _perform_search(self, query: str) -> list[ProductInfo]:
        # Search functionality is not direct on JITB site, usually we go to menu categories.
        # For this MVP, we will navigate to the generic menu page and search text.
        url = "https://www.jackinthebox.com/menu"
        self.driver.get(url)
        
        results = []
        try:
            # Wait for any content
            time.sleep(5) 
            
            # This is speculative as we couldn't confirm selectors
            # Looking for common patterns in Next.js apps
            elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '$')]")
            
            seen_names = set()
            
            for el in elements:
                try:
                    text = el.text
                    if "$" in text and len(text) < 20: # Short price text like "$5.50"
                         # Try to find the name nearby (sibling or parent-sibling)
                         # This is heuristic
                         parent = el.find_element(By.XPATH, "./..")
                         full_text = parent.text
                         lines = full_text.split('\n')
                         
                         name = "Unknown Item"
                         price = 0.0
                         
                         for line in lines:
                             if "$" in line:
                                 try:
                                    price = float(line.replace('$', '').strip())
                                 except:
                                     pass
                             elif len(line) > 3:
                                 name = line
                        
                         if name != "Unknown Item" and name not in seen_names and query.lower() in name.lower():
                             seen_names.add(name)
                             results.append({
                                 "name": name,
                                 "price": price,
                                 "unit": "item",
                                 "store": "Jack in the Box",
                                 "type": "restaurant",
                                 "nutrition": {}
                             })
                except:
                    continue
                    
            return results
        except Exception as e:
            logging.error(f"Error scraping Jack In The Box: {e}")
            return []
