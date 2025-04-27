# create products and propensity_to_buy lists from CSV data file
import csv
from typing import Dict, List, Any
from datetime import datetime
from stream_generator.business_logic.domain import modeling, exceptions
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
        for some_weight in bronze_data["quantity_weights"].split(";")
    ]

    return modeling.Product(**temp_dict)


def product_data_testing(silver_product: modeling.Product) -> None:
    if(silver_product.propensity_to_buy <= 0):
        raise exceptions.NoPositiveIntegerPropensityToBuyException()
    if( (silver_product.propensity_to_add_supplement < 0) or (silver_product.propensity_to_add_supplement > 1) ):
        raise exceptions.NoProbabilityPropensityToAddSupplementException()
    if(silver_product.price <= 0):
        raise exceptions.NoPositivePriceException()
    if(silver_product.cogs <= 0):
        raise exceptions.NoPositiveCOGSException()
    if(silver_product.min_inventory <= 0):
        raise exceptions.NonPositiveMinInventoryException()
    if(silver_product.inventory < silver_product.min_inventory):
        raise exceptions.InventoryBelowMinimumException()
    if(silver_product.restock_amount <= 0):
        raise exceptions.NonPositiveRestockAmountException()
    if( (silver_product.member_discount < 0) or (silver_product.member_discount > 1) ):
        raise exceptions.NonPercentageClubMemberDiscountException()
    if( (silver_product.member_probability < 0) or (silver_product.member_probability > 1) ):
        raise exceptions.NonProbabilityIsMemberProbException()
    if(silver_product.supplements_cost <= 0):
        raise exceptions.NonPositiveSupplementsCostException()
    if len(silver_product.quantity_weights) == 0:
        raise exceptions.EmptyQuantityWeights()
    for weight in silver_product.quantity_weights:
        if(weight <= 0):
            raise exceptions.NonPositiveQuantityWeightException()

    if len(silver_product.quantity_weights) > silver_product.min_inventory:
        raise exceptions.QuantityAboveInventoryException()

    if silver_product.restock_amount < silver_product.min_inventory:
        raise exceptions.RestockAmoundBelowMinInventoryException()

def products_data_testing(silver_products: List[modeling.Product]) -> None:
    if len(silver_products) == 0:
        raise exceptions.NoProductsException()

    all_product_ids = [product.product_id for product in silver_products]

    if(len(all_product_ids)) != len(all_product_ids):
        raise exceptions.NonUniqueProductIdsException()


def deserialize_product_list() -> List[modeling.Product]:
    products : List[modeling.Product] = []
    with open(Path(__file__).parent / "products.csv", "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"ROW is {row}")
            product = product_schema_enforcement(row)
            product_data_testing(product)
            products.append(product)

    products_data_testing(products)
    return products