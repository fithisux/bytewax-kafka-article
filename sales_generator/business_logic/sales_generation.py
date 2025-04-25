from business_logic.domain import modeling
from configuration_logic.sales_generator.domain.modeling import GeneratorConfig
from typing import List, Optional, Tuple
import random
from datetime import datetime

# generate synthetic sale transactions


def generate_choice_from_weights(weights: List[int]) -> int:
    population = list(range(0, len(weights)))
    return random.choices(population, weights, k=1)[0]


def generate_sales(
    products: List[modeling.Product], generator_config: GeneratorConfig
) -> Optional[Tuple[modeling.Purchase, Optional[modeling.Inventory]]]:

    sorted_products = products.sort(key=lambda product: product.propensity_to_buy)
    propensities = [product.propensity_to_buy for product in sorted_products]
    transaction_time = datetime.now()
    is_member = generator_config.is_member_prob <= random.random()
    member_discount = generator_config.club_member_discount if is_member else 0.00
    items = 1 + generate_choice_from_weights(generator_config.transaction_items_weights)

    for _ in range(0, items):
        # reduces but not eliminates risk of duplicate products in same transaction - TODO: improve this method
        product = random.choices(sorted_products, propensities)[0]
        quantity = 1 + generate_choice_from_weights(
            generator_config.transaction_quantity_weights
        )
        add_supplement = product.propensity_to_add_supplement <= random.random()
        supplement_price = generator_config.supplements_cost if add_supplement else 0.00
        new_purchase = modeling.Purchase(
            transaction_time,
            str(abs(hash(transaction_time))),
            product.product_id,
            product.price,
            quantity,
            is_member,
            member_discount,
            add_supplement,
            supplement_price,
        )
        product.inventory_level = product.inventory_level - quantity
        new_inventory = fix_product_inventory(product, generator_config)
        return (new_purchase, new_inventory)

    return None  # should never reach here


def fix_product_inventory(
    product: modeling.Product, generator_config: GeneratorConfig
) -> Optional[modeling.Inventory]:
    new_inventory: Optional[modeling.Inventory] = None
    if product.inventory_level < generator_config.min_inventory:
        new_level = product.inventory_level + generator_config.restock_amount
        new_inventory = modeling.Inventory(
            str(datetime.now()),
            product.product_id,
            product.inventory_level,
            generator_config.restock_amount,
            new_level,
        )
        product.inventory_level = new_level
    return new_inventory
