from sales_generator.business_logic.domain import modeling
from sales_generator.configuration_logic.data_generation.domain.modeling import GeneratorConfig
from typing import List, Optional, Tuple
import random
from datetime import datetime

# generate synthetic sale transactions


def generate_choice_from_weights(weights: List[int]) -> int:
    population = list(range(0, len(weights)))
    return random.choices(population, weights, k=1)[0]


def generate_sale(
    products: List[modeling.Product], generator_config: GeneratorConfig
) ->Tuple[Optional[modeling.Purchase], Optional[modeling.Inventory]]:

    propensities = [product.propensity_to_buy for product in products]
    transaction_time = datetime.now()
    is_member = generator_config.is_member_prob <= random.random()
    member_discount = generator_config.club_member_discount if is_member else 0.00
    items = 1 + generate_choice_from_weights(generator_config.transaction_items_weights)

    for _ in range(0, items):
        # reduces but not eliminates risk of duplicate products in same transaction - TODO: improve this method
        product = random.choices(products, propensities)[0]
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
        product.inventory_surplus = product.inventory_surplus - quantity
        new_inventory = fix_product_inventory(product, generator_config)
        return (new_purchase, new_inventory)

    return (None,None)  # should never reach here


def fix_product_inventory(
    product: modeling.Product, generator_config: GeneratorConfig
) -> Optional[modeling.Inventory]:
    new_inventory: Optional[modeling.Inventory] = None
    if product.inventory_surplus < 0:
        new_surplus = product.inventory_surplus + generator_config.min_inventory + generator_config.restock_amount
        new_inventory = modeling.Inventory(
            datetime.now(),
            product.product_id,
            product.inventory_surplus + generator_config.min_inventor,
            generator_config.restock_amount,
            new_surplus + generator_config.min_inventor,
        )
        product.inventory_surplus = new_surplus
    return new_inventory
