from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Optional
from .interface import ScraperInterface, ProductInfo
import logging

class SeleniumScraper(ScraperInterface):
    def __init__(self, headless: bool = True):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = None

    def _setup_driver(self):
        if not self.driver:
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.options
            )

    def _teardown_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def search(self, query: str) -> List[ProductInfo]:
        try:
            self._setup_driver()
            return self._perform_search(query)
        except Exception as e:
            logging.error(f"Error during search: {e}")
            return []
        finally:
            self._teardown_driver()

    def _perform_search(self, query: str) -> List[ProductInfo]:
        """Override this in subclasses"""
        return []
