from typing import Dict, Any, List
from .models import BenchmarkItem

class AnalysisEngine:
    @staticmethod
    def calculate_metrics(price: float, nutrition: Dict[str, Any], unit_weight_g: float = 100.0) -> Dict[str, float]:
        """
        Calculates key value metrics (per dollar) based on price and nutrition data.
        Assumes nutrition data is per 100g, or needs normalization.
        """
        if price <= 0:
            return {}

        # Safe extraction with defaults
        # We need to parse "5g" -> 5.0
        def parse_val(val):
            if isinstance(val, (int, float)):
                return float(val)
            if isinstance(val, str):
                # Remove non-numeric chars except .
                clean = "".join(c for c in val if c.isdigit() or c == '.')
                return float(clean) if clean else 0.0
            return 0.0

        calories = parse_val(nutrition.get("calories", 0))
        protein = parse_val(nutrition.get("protein", 0))
        fiber = parse_val(nutrition.get("fiber", 0)) # Assuming we get fiber
        
        # Calculate how many 100g servings you get for the total price?
        # Actually, usually we have: Price for X amount.
        # Let's assume 'price' is for 'unit_weight_g' for simplicity 
        # OR we calculate metrics per dollar directly.
        
        # If price is for 1 item, and item is 454g (1lb).
        # Nutrition is per 100g.
        # Total Calories = (Item Weight / 100) * Calories_per_100g
        # Calories Per Dollar = Total Calories / Price
        
        total_calories = (unit_weight_g / 100.0) * calories
        total_protein = (unit_weight_g / 100.0) * protein
        
        return {
            "calories_per_dollar": total_calories / price,
            "protein_per_dollar": total_protein / price,
            "price_per_100g": price / (unit_weight_g / 100.0)
        }

    @staticmethod
    def calculate_opportunity_cost(fast_food_item: Dict[str, Any], benchmark: BenchmarkItem) -> Dict[str, Any]:
        """
        Compares a fast food item against a benchmark item.
        Returns the 'Opportunity Cost' - i.e., how much MORE you could have gotten.
        """
        ff_price = fast_food_item.get("price", 0)
        if ff_price <= 0:
            return {}

        # Fast food nutrition (total for item)
        ff_nutrition = fast_food_item.get("nutrition", {})
        # Flatten fast food metrics
        # For fast food, nutrition is usually "per serving" (the whole item)
        # So we just take the raw values
        ff_cal = float(ff_nutrition.get("calories", 0))
        ff_prot = float(str(ff_nutrition.get("protein", "0")).replace('g',''))
        
        # Benchmark metrics are stored as "Per Dollar"
        # So for the SAME COST (ff_price), what could we get from benchmark?
        alt_cal = benchmark.calories_per_dollar * ff_price
        alt_prot = benchmark.protein_per_dollar * ff_price
        
        return {
            "cost": ff_price,
            "comparison_item": benchmark.name,
            "fast_food_metrics": {
                "calories": ff_cal,
                "protein": ff_prot
            },
            "benchmark_potential": {
                "calories": alt_cal,
                "protein": alt_prot,
                "quantity_lbs": (ff_price / benchmark.price_per_100g) * 100 / 453.592 # convert g to lbs
            },
            "multipliers": {
                "calories": alt_cal / ff_cal if ff_cal > 0 else 0,
                "protein": alt_prot / ff_prot if ff_prot > 0 else 0
            }
        }
