from typing import List, Dict, Any
from abc import ABC, abstractmethod

class ProductInfo(Dict[str, Any]):
    """
    Standardized dictionary for product info:
    {
        "name": str,
        "price": float,
        "unit": str,
        "store": str,
        "type": str, # "grocery" or "restaurant"
        "nutrition": dict
    }
    """
    pass

class ScraperInterface(ABC):
    @abstractmethod
    def search(self, query: str) -> List[ProductInfo]:
        pass
