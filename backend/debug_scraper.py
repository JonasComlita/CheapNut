from scrapers.base_selenium import SeleniumScraper
import time
import traceback
import sys

class DebugScraper(SeleniumScraper):
    def search(self, query: str):
        try:
            print("Setting up driver...")
            self._setup_driver()
            print("Driver setup complete. GET URL...")
            self.driver.get("https://www.jackinthebox.com/menu/categories")
            print("Waiting...")
            time.sleep(5)
            print("Writing file...")
            with open("jack_dump.html", "w") as f:
                f.write(self.driver.page_source)
            print("Done.")
            return []
        except Exception:
            traceback.print_exc()
            return []
        finally:
            self._teardown_driver()

if __name__ == "__main__":
    s = DebugScraper()
    s.search("test")
