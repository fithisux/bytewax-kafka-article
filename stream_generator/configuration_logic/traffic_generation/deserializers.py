import configparser
from stream_generator.configuration_logic.traffic_generation.domain import modeling, exceptions
from pathlib import Path
from typing import Tuple


def deserialize() -> modeling.TrafficConfig:
    config = configparser.ConfigParser()

    config_path = Path(__file__).parent
    config.read(config_path / "configuration.ini")
    min_sale_freq = int(config["SALES"]["min_sale_freq"])
    max_sale_freq = int(config["SALES"]["max_sale_freq"])
    number_of_sales = int(config["SALES"]["number_of_sales"])
    transaction_items_weights = [
        int(some_weight)
        for some_weight in config["SALES"]["transaction_items_weights"].split(",")
    ]

    traffic_config = modeling.TrafficConfig(
        min_sale_freq, max_sale_freq, number_of_sales, transaction_items_weights
    )

    return traffic_config


def traffic_configuration_data_testing(traffic_config: modeling.TrafficConfig) -> None:
    
    if(traffic_config.number_of_sales <= 0):
        raise exceptions.NonPositiveNumSalesException()

    if(traffic_config.min_sale_freq <= 0):
        raise exceptions.NonPositiveMinSaleFrequenceException()
    if(traffic_config.max_sale_freq <= 0):
        raise exceptions.NonPositiveMaxSaleFrequencyException()

    if(traffic_config.max_sale_freq < traffic_config.min_sale_freq):
        raise exceptions.MinMaxSaleFrequencyException()

    if len(traffic_config.transaction_items_weights) == 0:
        raise exceptions.EmptyTransactionItemsWeights()

    for weight in traffic_config.transaction_items_weights:
        if(weight <= 0):
            raise exceptions.NonPositiveTransactionItemsWeightException()