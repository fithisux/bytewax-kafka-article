from dataclasses import dataclass
from typing import List

@dataclass
class GeneratorConfig:
    transaction_items_weights: List[int]
    transaction_quantity_weights: List[int]
    min_inventory: int
    restock_amount : int
    is_member_prob: float
    club_member_discount: float
    supplements_cost: float


@dataclass
class TrafficConfig:
    min_sale_freq: int
    max_sale_freq: int
    number_of_sales: int