import configparser
from stream_generator.configuration_logic.traffic_generation.domain import modeling, datatesting
from pathlib import Path


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

    datatesting.traffic_configuration_data_testing(traffic_config)

    return traffic_config