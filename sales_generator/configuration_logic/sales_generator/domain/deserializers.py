import configparser
from configuration_logic import sales_generator
from configuration_logic.sales_generator.domain import modeling, exceptions
from pathlib import Path
from typing import Tuple


def get_config() -> Tuple[modeling.GeneratorConfig, modeling.TrafficConfig]:
    config = configparser.ConfigParser()

    config_path = Path(sales_generator.__file__).parent
    config.read(config_path / "configuration.ini")
    min_sale_freq = int(config["SALES"]["min_sale_freq"])
    max_sale_freq = int(config["SALES"]["max_sale_freq"])
    number_of_sales = int(config["SALES"]["number_of_sales"])
    traffic_config = modeling.TrafficConfig(
        min_sale_freq, max_sale_freq, number_of_sales
    )

    transaction_items_weights = [
        int(some_weight)
        for some_weight in config["SALES"]["transaction_items_weights"].split(";")
    ]
    transaction_quantity_weights = [
        int(some_weight)
        for some_weight in config["SALES"]["transaction_quantity_weights"].split(";")
    ]
    is_member_prob = float(config["SALES"]["is_member_prob"])
    club_member_discount = float(config["SALES"]["club_member_discount"])
    supplements_cost = float(config["SALES"]["supplements_cost"])
    min_inventory = int(config["INVENTORY"]["min_inventory"])
    restock_amount = int(config["INVENTORY"]["restock_amount"])

    generator_config = modeling.GeneratorConfig(
        transaction_items_weights,
        transaction_quantity_weights,
        min_inventory,
        restock_amount,
        is_member_prob,
        club_member_discount,
        supplements_cost,
    )

    return (generator_config, traffic_config)


def generator_configuration_data_testing(generator_config: modeling.GeneratorConfig) -> None:
    if(generator_config.min_inventory <= 0):
        raise exceptions.NonPositiveMinInventoryException()
    if(generator_config.restock_amount <= 0):
        raise exceptions.NonPositiveRestockAmountException()
    if( (generator_config.club_member_discount < 0) or (generator_config.club_member_discount > 0) ):
        raise exceptions.NonPercentageClubMemberDiscountException()
    if( (generator_config.is_member_prob < 0) or (generator_config.is_member_prob > 0) ):
        raise exceptions.NonProbabilityIsMemberProbException()
    if(generator_config.supplements_cost <= 0):
        raise exceptions.NonPositiveSupplementsCostException()
    if len(generator_config.transaction_items_weights) == 0:
        raise exceptions.EmptyTransactionItemsWeights()

    for weight in generator_config.transaction_items_weights:
        if(weight <= 0):
            raise exceptions.NonPositiveTransactionItemsWeightException()

    if len(generator_config.transaction_quantity_weights) == 0:
        raise exceptions.EmptyTransactionQuantityWeights()

    for weight in generator_config.transaction_quantity_weights:
        if(weight <= 0):
            raise exceptions.NonPositiveTransactionQuantityWeightException()


def traffic_configuration_data_testing(traffic_config: modeling.TrafficConfig) -> None:
    
    if(traffic_config.number_of_sales <= 0):
        raise exceptions.NonPositiveNumSalesException()

    if(traffic_config.min_sale_freq <= 0):
        raise exceptions.NonPositiveMinSaleFrequenceException()
    if(traffic_config.max_sale_freq <= 0):
        raise exceptions.NonPositiveMaxSaleFrequencyException()

    if(traffic_config.max_sale_freq < traffic_config.min_sale_freq):
        raise exceptions.MinMaxSaleFrequencyException()