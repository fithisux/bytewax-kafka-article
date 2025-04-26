from dataclasses import dataclass
from datetime import datetime

@dataclass
class Inventory:
    event_time: datetime
    product_id: str
    existing_level: int
    stock_quantity: int
    new_level: int



@dataclass
class Product:
    event_time: datetime
    product_id: str
    category: str
    item: str
    size: str
    cogs: float
    price: float
    inventory_surplus: int
    contains_fruit: bool
    contains_veggies: bool
    contains_nuts: bool
    contains_caffeine: bool
    propensity_to_buy: int
    propensity_to_add_supplement: float


@dataclass
class Purchase:
    transaction_time: datetime
    transaction_id: str
    product_id: str
    price: float
    quantity: int
    is_member: bool
    member_discount: float
    add_supplements: bool
    supplement_price: float