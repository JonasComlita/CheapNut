from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Enum
from sqlalchemy.sql import func
import enum
from database import Base

class ItemType(str, enum.Enum):
    grocery = "grocery"
    restaurant = "restaurant"

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    item_type = Column(String, index=True) # grocery or restaurant
    store_name = Column(String, index=True)
    price = Column(Float)
    unit = Column(String) # e.g. "lb", "oz", "item"
    quantity = Column(Float) # Amount of unit, e.g. 2 (lbs)
    
    # Nutrition data per 100g or per serving? 
    # Let's aim for per 100g standard, or store serving size info.
    # Storing raw JSON from API for flexibility.
    nutrition_data = Column(JSON) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=True) # Future proofing
    name = Column(String) # e.g. "Chicken Dinner"
    
    # Storing snapshot of calculation or references to items?
    # For now, let's store the result
    savings = Column(Float)
    nutrition_diff = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BenchmarkItem(Base):
    __tablename__ = "benchmark_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # e.g. "Frozen Green Beans"
    lowest_price = Column(Float)
    unit = Column(String) # e.g. "lb"
    store = Column(String) # e.g. "Walmart"
    
    # Normalized metrics for comparison
    price_per_100g = Column(Float)
    calories_per_dollar = Column(Float)
    protein_per_dollar = Column(Float)
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

