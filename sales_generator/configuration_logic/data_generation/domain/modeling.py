from dataclasses import dataclass
from typing import List

@dataclass
class GeneratorConfig:
    transaction_items_weights: List[int]


@dataclass
class TrafficConfig:
    min_sale_freq: int
    max_sale_freq: int
    number_of_sales: int