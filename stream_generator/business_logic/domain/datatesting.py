from typing import List
from stream_generator.business_logic.domain import modeling, exceptions

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
    if(silver_product.supplement_cost <= 0):
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