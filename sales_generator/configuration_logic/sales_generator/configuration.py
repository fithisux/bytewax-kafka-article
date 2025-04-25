import configparser
import generator_config
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class GeneratorConfig:
    min_sale_freq: int
    max_sale_freq: int
    number_of_sales: int
    transaction_items_weights: List[int]
    transaction_quantity_weights: List[int]
    min_inventory: int
    restock_amount : int
    is_member_prob: float
    club_member_discount: float
    supplements_cost: float

def get_configs():
    config = configparser.ConfigParser()

    config_path = Path(generator_config.__file__).parent
    config.read(config_path / "configuration.ini")
    min_sale_freq = int(config["SALES"]["min_sale_freq"])
    max_sale_freq = int(config["SALES"]["max_sale_freq"])
    number_of_sales = int(config["SALES"]["number_of_sales"])
    transaction_items_weights = int(
    config["SALES"]["transaction_items_weights"]
    )
    transaction_quantity_weights = int(config["SALES"]["transaction_quantity_weights"])
    is_member_prob = float(config["SALES"]["is_member_prob"])
    club_member_discount = float(config["SALES"]["club_member_discount"])
    supplements_cost = float(config["SALES"]["supplements_cost"])
    min_inventory = int(config["INVENTORY"]["min_inventory"])
    restock_amount = int(config["INVENTORY"]["restock_amount"])