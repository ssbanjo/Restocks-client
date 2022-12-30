from dataclasses import dataclass
from datetime import datetime
import re
from typing import NamedTuple, Optional, Self
from .utils.helpers import parse_int, parse_size

SIZES_IDS = {"35.5": 54, "36": 1, "36.5": 13, "37.5": 44, "38": 3, "38.5": 48, "39": 4, "40": 5, "40.5": 22, "41": 6, "42": 7, "42.5": 23, "43": 8, "44": 9, "44.5": 24, "45": 10, "45.5": 41, "46": 11, "47": 49, "47.5": 25, "48": 21, "48.5": 26, "49.5": 42}

def _image_to_slug(image: str) -> str:
    
    return "https://restocks.net/p/" + re.sub("-[0-9]+-[0-9]+.png", "", image.split("/")[-1])

def _image_to_sku(image: str) -> str:
    
    return re.findall('/products/(.*?)/', image)[0]
    

class Variant(NamedTuple):
    
    size: str
    price: Optional[int]
    oos: bool

    @classmethod
    def _from_json(cls, data: dict):
        
        for size, price in data.items():
            
            yield Variant(size=size, price=price, oos=not price)
            
@dataclass
class Product:
    
    name: str
    sku: str
    slug: str
    image: str
    id: int
    price: int
    
    listing_id: Optional[int]
    size: Optional[str]
    variants: Optional[list[Variant]]
    date: Optional[datetime]
    
    @classmethod
    def _from_json(cls, data: dict) -> Self:
        
        return Product(
            name=data["name"],
            image=data["image"],
            slug=_image_to_slug(data["image"]),
            sku=_image_to_sku(data["image"]),
            id=parse_int(data["id"]),
            price=parse_int(data["storeprice"]),
            listing_id=parse_int(data["listing_id"]) if data.get("listing_id") else None,
            size=parse_size(data["size"]) if data.get("size") else None,
            variants=[v for v in Variant._from_json(data["variants"])] if data.get("variants") else None,
            date=datetime.strptime(data["date"], "%d/%m/%y") if data.get("date") else None
        )