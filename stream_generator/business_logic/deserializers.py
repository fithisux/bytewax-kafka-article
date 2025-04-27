# create products and propensity_to_buy lists from CSV data file
import csv
from typing import Dict, List, Any
from datetime import datetime
from stream_generator.business_logic.domain import modeling, datatesting
from pathlib import Path

def product_schema_enforcement(bronze_data: Dict[str, str]) -> modeling.Product:
    temp_dict: Dict[str, Any] = {}
    temp_dict["event_time"] = datetime.now()
    temp_dict["product_id"] = bronze_data["ID"]
    temp_dict["inventory"] = int(bronze_data["InitialInventory"])
    temp_dict["min_inventory"] = int(bronze_data["MinInventory"])
    temp_dict["restock_amount"] = int(bronze_data["RestockAmount"])
    temp_dict["propensity_to_buy"] = int(bronze_data["PropensityToBuy"])
    temp_dict["category"] = bronze_data["Category"]
    temp_dict["item"] = bronze_data["Item"]
    temp_dict["size"] = bronze_data["Size"]
    temp_dict["cogs"] = float(bronze_data["COGS"])
    temp_dict["price"] = float(bronze_data["Price"])
    temp_dict["member_probability"] = float(bronze_data["MemberProbability"])
    temp_dict["member_discount"] = float(bronze_data["MemberDiscount"])
    temp_dict["propensity_to_add_supplement"] = float(bronze_data["PropensityToAddSuplement"])
    temp_dict["supplement_cost"] = float(bronze_data["SupplementCost"])
    temp_dict["quantity_weights"] = [
        int(some_weight)
        for some_weight in bronze_data["QuantityWeights"].split(";")
    ]

    return modeling.Product(**temp_dict)


def deserialize_product_list() -> List[modeling.Product]:
    products : List[modeling.Product] = []
    with open(Path(__file__).parent / "products.csv", "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"ROW is {row}")
            product = product_schema_enforcement(row)
            datatesting.product_data_testing(product)
            products.append(product)

    datatesting.products_data_testing(products)
    return products