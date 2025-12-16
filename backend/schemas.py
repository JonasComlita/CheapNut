from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    item_type: str
    store_name: str
    price: float
    unit: str
    quantity: float
    nutrition_data: Optional[Dict[str, Any]] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ComparisonBase(BaseModel):
    name: str
    savings: float
    nutrition_diff: Optional[Dict[str, Any]] = None

class ComparisonCreate(ComparisonBase):
    pass

class Comparison(ComparisonBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
