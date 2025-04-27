from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Restock:
    event_time: datetime
    product_id: str
    existing_level: int
    stock_quantity: int
    new_level: int



@dataclass
class Product:
    event_time: datetime
    product_id: str
    inventory: int
    min_inventory: int
    restock_amount: int
    propensity_to_buy: int
    category: str
    item: str
    size: str
    cogs: float
    price: float
    member_probability: float
    member_discount: float
    propensity_to_add_supplement: float
    supplements_cost: float
    quantity_weights: List[int]


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