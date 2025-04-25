import configparser
import kafka_config
from pathlib import Path

def get_configs():
    config = configparser.ConfigParser()

    config_path = Path(kafka_config.__file__).parent
    config.read(config_path / "configuration.ini")

    bootstrap_servers = config["KAFKA"]["bootstrap_servers"]
    auth_method = config["KAFKA"]["auth_method"]
    sasl_username = config["KAFKA"]["sasl_username"]
    sasl_password = config["KAFKA"]["sasl_password"]

    configs = {"bootstrap_servers": bootstrap_servers}

    if auth_method == "sasl_scram":
        configs["security_protocol"] = "SASL_SSL"
        configs["sasl_mechanism"] = "SCRAM-SHA-512"
        configs["sasl_plain_username"] = sasl_username
        configs["sasl_plain_password"] = sasl_password

    config['topic_products'] = config["KAFKA"]["topic_products"]
    config['topic_purchases'] = config["KAFKA"]["topic_purchases"]
    config['topic_inventories'] = config["KAFKA"]["topic_inventories"]


    # print("configs: {0}".format(str(configs)))

    return configs
