from stream_generator.business_logic.domain import modeling
from typing import List, Optional, Tuple
import random
from datetime import datetime

def generate_choice_from_weights(weights: List[int]) -> int:
    population = list(range(0, len(weights)))
    return random.choices(population, weights, k=1)[0]


def generate_sales(
    products: List[modeling.Product], items: int
) -> List[Tuple[modeling.Purchase, Optional[modeling.Restock]]]:

    propensities = [product.propensity_to_buy for product in products]
    transaction_time = datetime.now()
    sale: List[Tuple[modeling.Purchase, Optional[modeling.Restock]]] = []
    for _ in range(0, items):
        product = random.choices(products, propensities)[0]

        is_member = product.member_probability <= random.random()
        member_discount = product.member_discount if is_member else 0.00
        # reduces but not eliminates risk of duplicate products in same transaction - TODO: improve this method
        
        quantity = 1 + generate_choice_from_weights(
            product.quantity_weights
        )
        add_supplement = product.propensity_to_add_supplement <= random.random()
        supplement_price = product.supplements_cost if add_supplement else 0.00
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
        product.inventory = product.inventory - quantity
        new_restock = fix_product_inventory(product)
        sale.append( (new_purchase, new_restock) )

    return sale


def fix_product_inventory(
    product: modeling.Product
) -> Optional[modeling.Restock]:
    new_restock: Optional[modeling.Restock] = None
    if product.inventory < product.min_inventory:
        new_inventory = product.inventory + product.restock_amount
        new_restock = modeling.Restock(
            datetime.now(),
            product.product_id,
            product.inventory,
            product.restock_amount,
            new_inventory,
        )
        product.inventory = new_inventory
    return new_restock
