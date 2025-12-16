from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CheapNut API")

origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from scrapers.mock_scraper import MockGroceryScraper, MockFastFoodScraper
from scrapers.walmart import WalmartScraper
from scrapers.jack_in_the_box import JackInTheBoxScraper
from scrapers.safeway import SafewayScraper
from scrapers.whole_foods import WholeFoodsScraper
from scrapers.target import TargetScraper
from scrapers.costco import CostcoScraper
from scrapers.trader_joes import TraderJoesScraper
from scrapers.mcdonalds import McDonaldsScraper
from scrapers.taco_bell import TacoBellScraper
from scrapers.starbucks import StarbucksScraper
from scrapers.chipotle import ChipotleScraper
from nutrition_service import NutritionService
from typing import List

@app.get("/")
def read_root():
    return {"message": "Welcome to CheapNut API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/search")
def search_items(q: str):
    # Initialize scrapers (Note: In prod, these should be singleton or pooled)
    walmart = WalmartScraper(headless=True)
    jitb = JackInTheBoxScraper(headless=True)
    safeway = SafewayScraper(headless=True)
    wholefoods = WholeFoodsScraper(headless=True)
    target = TargetScraper(headless=True)
    costco = CostcoScraper(headless=True)
    traderjoes = TraderJoesScraper(headless=True)
    mcdonalds = McDonaldsScraper(headless=True)
    tacobell = TacoBellScraper(headless=True)
    starbucks = StarbucksScraper(headless=True)
    chipotle = ChipotleScraper(headless=True)
    
    # Fallback/Mock for others for now
    mock_grocery = MockGroceryScraper()
    mock_fastfood = MockFastFoodScraper()
    
    # Run searches
    results = {
        "grocery": [],
        "fastfood": []
    }
    
    # Grocery
    results["grocery"].extend(walmart.search(q))
    results["grocery"].extend(safeway.search(q))
    results["grocery"].extend(wholefoods.search(q))
    results["grocery"].extend(target.search(q))
    results["grocery"].extend(costco.search(q))
    results["grocery"].extend(traderjoes.search(q))

    # Fallback if empty
    if not results["grocery"]:
        results["grocery"] = mock_grocery.search(q)
        
    # Fast Food
    results["fastfood"].extend(jitb.search(q))
    results["fastfood"].extend(mcdonalds.search(q))
    results["fastfood"].extend(tacobell.search(q))
    results["fastfood"].extend(starbucks.search(q))
    results["fastfood"].extend(chipotle.search(q))
    
    if not results["fastfood"]:
        results["fastfood"] = mock_fastfood.search(q)

    # Enrich with Nutrition Data
    nutrition_service = NutritionService()
    
    # We can limit nutrition calls to top 3 items per category to save time/rate limits
    for category in ["grocery", "fastfood"]:
        for item in results[category][:3]:
            # Use the item name for nutrition lookup
            # Cleanup name slightly? 
            clean_name = item["name"].split(',')[0] 
            item["nutrition"] = nutrition_service.get_nutrition(clean_name)

    return results

# --- New Best Value Endpoints ---

from smart_pantry import update_benchmarks
from database import get_db, engine
from models import Base, BenchmarkItem
from analysis_engine import AnalysisEngine
from sqlalchemy.orm import Session
from fastapi import Depends, BackgroundTasks

# Ensure tables exist (dev convenience)
Base.metadata.create_all(bind=engine) 

@app.post("/api/benchmarks/refresh")
def refresh_benchmarks(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Triggers a background task to update staple prices.
    """
    background_tasks.add_task(update_benchmarks, db)
    return {"message": "Benchmark update started in background"}

@app.get("/api/benchmarks/leaderboard")
def get_leaderboard(metric: str = "protein_per_dollar", db: Session = Depends(get_db)):
    """
    Returns top items sorted by the requested metric.
    Metric options: protein_per_dollar, calories_per_dollar, lowest_price
    """
    # Map friendly query param to column
    metric_map = {
        "protein": BenchmarkItem.protein_per_dollar,
        "calories": BenchmarkItem.calories_per_dollar,
        "price": BenchmarkItem.lowest_price
    }
    
    sort_col = metric_map.get(metric, BenchmarkItem.protein_per_dollar)
    
    # Sort Descending for value, Ascending for price?
    # Usually we want "More per dollar" -> Descending
    if metric == "price":
        items = db.query(BenchmarkItem).order_by(sort_col.asc()).limit(10).all()
    else:
        items = db.query(BenchmarkItem).order_by(sort_col.desc()).limit(10).all()
        
    return items

@app.get("/api/compare/opportunity-cost")
def compare_item(query: str, db: Session = Depends(get_db)):
    """
    Compares a fast food query against the 'best' protein benchmark.
    """
    # 1. Get Fast Food Info
    # Use generic scrapers or mock for now
    # Ideally reuse the search_items logic but strictly for 1 item
    pass  # To be implemented cleanly, reusing search logic or a new helper

    # Reuse the search function logic? Or create a helper.
    # Let's instantiate a quick scraper or use the existing 'search_items' logic if refactored.
    # For MVP, let's just do a quick McDonald's search
    
    mcd = McDonaldsScraper(headless=True)
    results = mcd.search(query)
    mcd.driver.quit()
    
    if not results:
        return {"error": "Item not found"}
        
    target_item = results[0]  # Take top result
    
    # Enrich
    nut_service = NutritionService()
    target_item["nutrition"] = nut_service.get_nutrition(target_item["name"])
    
    # 2. Get Benchmark
    # Compare against best protein per dollar item
    benchmark = db.query(BenchmarkItem).order_by(BenchmarkItem.protein_per_dollar.desc()).first()
    
    if not benchmark:
        return {"error": "No benchmarks available. Run refresh first."}
        
    # 3. Calculate
    analysis = AnalysisEngine.calculate_opportunity_cost(target_item, benchmark)
    
    return analysis

