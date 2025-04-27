from dataclasses import dataclass
from typing import List  


@dataclass
class TrafficConfig:
    min_sale_freq: int
    max_sale_freq: int
    number_of_sales: int
    transaction_items_weights: List[int]
