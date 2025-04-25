# create products and propensity_to_buy lists from CSV data file
import csv
from typing import Dict, List, Any
from datetime import datetime
from business_logic.domain import modeling, exceptions

# convert uppercase boolean values from CSV file to Python
def to_bool(value):
    if type(value) is str and str(value).lower() == "true":
        return True
    return False


def product_schema_enforcement(bronze_data: Dict[str, str]) -> modeling.Product:
    temp_dict: Dict[str, Any] = {}
    temp_dict["event_time"] = datetime.now()
    temp_dict["product_id"] = bronze_data["ID"]
    temp_dict["category"] = bronze_data["Category"]
    temp_dict["item"] = bronze_data["Item"]
    temp_dict["size"] = bronze_data["Size"]

    temp_dict["cogs"] = float(bronze_data["COGS"])
    temp_dict["price"] = float(bronze_data["Price"])
    temp_dict["inventory_level"] = float(bronze_data["Inventory"])

    temp_dict["contains_fruit"] = to_bool(bronze_data["ContainsFruit"])
    temp_dict["contains_veggies"] = to_bool(bronze_data["ContainsVeggies"])
    temp_dict["contains_nuts"] = to_bool(bronze_data["ContainsNuts"])
    temp_dict["contains_caffeine"] = to_bool(bronze_data["ContainsCaffeine"])

    temp_dict["propensity_to_buy"] = int(bronze_data["PropensityToBuy"])
    temp_dict["propensity_to_add_supplement"] = float(bronze_data["PropensityToAddSuplement"])

    return modeling.Product(**temp_dict)


def product_data_testing(silver_product: modeling.Product, min_inventory_level: int) -> None:
    if(silver_product.propensity_to_buy <= 0):
        raise exceptions.NoPositiveIntegerPropensityToBuyException()
    if( (silver_product.propensity_to_add_supplement < 0) or (silver_product.propensity_to_add_supplement > 1) ):
        raise exceptions.NoProbabilityPropensityToAddSupplementException()
    if(silver_product.price <= 0):
        raise exceptions.NoPositivePriceException()
    if(silver_product.cogs <= 0):
        raise exceptions.NoPositiveCOGSException()
    if(silver_product.inventory_level <= 0):
        raise exceptions.NoPositiveInventoryException()
    if(silver_product.inventory_level < min_inventory_level):
        raise exceptions.TooSmallInventoryLevelException()

def products_data_testing(silver_products: List[modeling.Product]) -> None:
    if len(silver_products) == 0:
        raise exceptions.NoProductsException()

    all_product_ids = [product.product_id for product in silver_products]

    if(len(all_product_ids)) != len(all_product_ids):
        raise exceptions.NonUniqueProductIdsException()


def deserialize_product_list(min_inventory_level: int) -> List[modeling.Product]:
    products : List[modeling.Product] = []
    with open("data/products.csv", "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product = product_schema_enforcement(row)
            product_data_testing(product, min_inventory_level)
            products.append(product)

    products_data_testing(products)
    return products