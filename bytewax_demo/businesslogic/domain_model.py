from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

@dataclass
class SubTotal:
    product_id: str
    event_time: str
    transactions: int
    quantities: int
    sales: float

@dataclass
class Total:
    transactions: int
    quantities: int
    sales: float

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

