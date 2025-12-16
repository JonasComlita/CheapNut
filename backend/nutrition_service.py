import requests
import logging
from typing import Dict, Any, Optional

class NutritionService:
    def get_nutrition(self, query: str) -> Dict[str, Any]:
        """
        Fetch nutrition data from OpenFoodFacts based on a query string.
        Returns a dictionary of relevant nutrients.
        """
        try:
            # OpenFoodFacts Search API
            url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1"
            response = requests.get(url, headers={"User-Agent": "CheapNut/1.0 (Integration Test)"}, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                
                if products:
                    # Get the first relevant product
                    product = products[0]
                    nutriments = product.get('nutriments', {})
                    
                    return {
                        "calories": nutriments.get("energy-kcal_100g", 0),
                        "protein": f"{nutriments.get('proteins_100g', 0)}g",
                        "carbohydrates": f"{nutriments.get('carbohydrates_100g', 0)}g",
                        "fat": f"{nutriments.get('fat_100g', 0)}g",
                        "vitamin_a": f"{nutriments.get('vitamin-a_100g', 0)}g",
                        "vitamin_c": f"{nutriments.get('vitamin-c_100g', 0)}g",
                        "iron": f"{nutriments.get('iron_100g', 0)}g",
                        "calcium": f"{nutriments.get('calcium_100g', 0)}g",
                        "serving_size": product.get("serving_size", "100g")
                    }
            
            return {}
        except Exception as e:
            logging.error(f"Error fetching nutrition for {query}: {e}")
            return {}
