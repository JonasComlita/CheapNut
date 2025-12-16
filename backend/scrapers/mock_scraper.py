from typing import List
from .interface import ScraperInterface, ProductInfo
import random

class MockGroceryScraper(ScraperInterface):
    def search(self, query: str) -> List[ProductInfo]:
        # Mock data based on user example
        results = []
        if "bean" in query.lower():
            results.append({
                "name": "Frozen Green Beans",
                "price": 1.50, # $3 for 2 lbs -> 1.5/lb
                "unit": "lb",
                "store": "Walmart",
                "type": "grocery",
                "nutrition": {"calories": 30, "vitamin_a": "15%", "vitamin_c": "20%"}
            })
        if "chicken" in query.lower():
            results.append({
                "name": "Chicken Thighs",
                "price": 2.50,
                "unit": "lb",
                "store": "Safeway",
                "type": "grocery",
                "nutrition": {"calories": 200, "protein": "25g"}
            })
        
        return results

class MockFastFoodScraper(ScraperInterface):
    def search(self, query: str) -> List[ProductInfo]:
        results = []
        if "sandwich" in query.lower() or "croissant" in query.lower():
             results.append({
                "name": "Sausage Croissant Sandwich",
                "price": 2.75,
                "unit": "item",
                "store": "Jack in the Box",
                "type": "restaurant",
                "nutrition": {"calories": 450, "fat": "30g", "sodium": "800mg"}
            })
        return results
