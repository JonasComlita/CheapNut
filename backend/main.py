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

from .scrapers.mock_scraper import MockGroceryScraper, MockFastFoodScraper
from .scrapers.walmart import WalmartScraper
from .scrapers.jack_in_the_box import JackInTheBoxScraper
from .scrapers.safeway import SafewayScraper
from .scrapers.whole_foods import WholeFoodsScraper
from .scrapers.target import TargetScraper
from .scrapers.costco import CostcoScraper
from .scrapers.trader_joes import TraderJoesScraper
from .scrapers.mcdonalds import McDonaldsScraper
from .scrapers.taco_bell import TacoBellScraper
from .scrapers.starbucks import StarbucksScraper
from .scrapers.chipotle import ChipotleScraper
from .nutrition_service import NutritionService
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
