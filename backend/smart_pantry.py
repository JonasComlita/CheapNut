from typing import List, Dict
import logging
from sqlalchemy.orm import Session
from models import BenchmarkItem
from scrapers.walmart import WalmartScraper
from scrapers.safeway import SafewayScraper
from scrapers.trader_joes import TraderJoesScraper
from nutrition_service import NutritionService
from analysis_engine import AnalysisEngine

# List of high-efficiency staple items to track for benchmarking
STAPLE_ITEMS: List[Dict[str, str]] = [
    {"name": "Frozen Green Beans", "category": "frozen_sides"},
    {"name": "Frozen Mixed Vegetables", "category": "frozen_sides"},
    {"name": "Frozen Spinach", "category": "frozen_sides"},
    {"name": "Dried Lentils", "category": "pantry_stable"},
    {"name": "Dried Black Beans", "category": "pantry_stable"},
    {"name": "Brown Rice", "category": "pantry_stable"},
    {"name": "Rolled Oats", "category": "pantry_stable"},
    {"name": "Bananas", "category": "produce"},
    {"name": "Carrots", "category": "produce"},
    {"name": "Eggs", "category": "dairy"},
    {"name": "Whole Milk", "category": "dairy"},
    {"name": "Chicken Breast", "category": "meat"},
    {"name": "Canned Tuna", "category": "pantry_stable"},
    {"name": "Peanut Butter", "category": "pantry_stable"},
    {"name": "Whole Wheat Bread", "category": "bakery"}
]

def get_staple_queries() -> List[str]:
    """Returns a list of search queries for the staple items."""
    return [item["name"] for item in STAPLE_ITEMS]

def update_benchmarks(db: Session):
    """
    Iterates through staple items, scrapes current prices,
    gets nutrition info, and updates BenchmarkItems in DB.
    """
    logging.info("Starting Benchmark Update Routine...")
    
    # Initialize Scrapers
    # We use Walmart as primary for low prices, potentially others later
    walmart = WalmartScraper(headless=True)
    nutrition_service = NutritionService()
    
    for item in STAPLE_ITEMS:
        query = item["name"]
        logging.info(f"Updating benchmark for: {query}")
        
        # 1. Scrape Price
        # Try Walmart first
        results = walmart.search(query)
        
        if not results:
            logging.warning(f"No results found for {query}")
            continue
            
        # Find cheapest valid result
        # Simple heuristic: cheapest non-zero price
        valid_results = [r for r in results if r['price'] > 0]
        if not valid_results:
            continue
            
        best_deal = min(valid_results, key=lambda x: x['price'])
        
        # 2. Get Nutrition
        # We search OpenFoodFacts for generic nutrition of this item name
        # We use the generic 'query' name to avoid specific brand noise if possible,
        # OR we use the scraped name. Let's use the scraped name for accuracy, 
        # but sometimes 'Great Value Frozen Green Beans' is better than just 'Green Beans'
        nutrition = nutrition_service.get_nutrition(best_deal['name'])
        
        if not nutrition:
            # Fallback to query name
             nutrition = nutrition_service.get_nutrition(query)
             
        if not nutrition:
            logging.warning(f"No nutrition data for {query}")
            continue

        # 3. Calculate Metrics
        # Need to estimate weight. 
        # If 'unit' is 'item', we need to parse weight from title (e.g. "12 oz").
        # This is tricky. For now, let's assume standard package sizes or try to parse.
        # Quick hack: default to 454g (1lb) if unknown, or 100g if it looks small.
        # Ideally our scraper returns 'unit_string' like '16 oz'.
        # Walmart scraper returns 'unit': 'item'.
        # We will assume 1lb (454g) for most bulk items for MVP, or parse from title.
        
        estimated_weight_g = 454.0 # Default 1lb
        name_lower = best_deal['name'].lower()
        if '12 oz' in name_lower: estimated_weight_g = 340.0
        if '16 oz' in name_lower or '1 lb' in name_lower: estimated_weight_g = 454.0
        if '32 oz' in name_lower or '2 lb' in name_lower: estimated_weight_g = 907.0
        if '5 lb' in name_lower: estimated_weight_g = 2268.0
        
        metrics = AnalysisEngine.calculate_metrics(best_deal['price'], nutrition, estimated_weight_g)
        
        if not metrics:
            continue
            
        # 4. Save to DB
        # Check if exists
        db_item = db.query(BenchmarkItem).filter(BenchmarkItem.name == query).first()
        if not db_item:
            db_item = BenchmarkItem(name=query)
            db.add(db_item)
            
        db_item.lowest_price = best_deal['price']
        db_item.store = best_deal['store']
        db_item.unit = best_deal['unit']
        db_item.price_per_100g = metrics.get('price_per_100g', 0)
        db_item.calories_per_dollar = metrics.get('calories_per_dollar', 0)
        db_item.protein_per_dollar = metrics.get('protein_per_dollar', 0)
        
        db.commit()
        logging.info(f"Updated {query}: ${best_deal['price']} - {metrics.get('protein_per_dollar'):.1f}g prot/$")

    walmart.driver.quit()
    logging.info("Benchmark Update Complete.")
