import configparser
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class KafkaConnectionConfig:
    bootstrap_servers: str
    security_protocol: str | None = None
    sasl_mechanism: str | None = None
    sasl_plain_username: str | None = None
    sasl_plain_password: str | None = None

@dataclass
class KafkaConfig:
    kafka_connection_config: KafkaConnectionConfig
    topic_products: str
    topic_purchases: str
    topic_restocks: str



def get_config() -> KafkaConfig:
    config = configparser.ConfigParser()

    config_path = Path(__file__).parent
    config.read(config_path / "configuration.ini")

    bootstrap_servers = config["KAFKA"]["bootstrap_servers"]
    configs: Dict[str, str] = {"bootstrap_servers": bootstrap_servers}
    configs["security_protocol"] = "PLAINTEXT"

    kafka_connection_config: KafkaConnectionConfig = KafkaConnectionConfig(**configs)

    extra_configs: Dict[str, Any] = {'kafka_connection_config' : kafka_connection_config}

    extra_configs['topic_products'] = config["KAFKA"]["topic_products"]
    extra_configs['topic_purchases'] = config["KAFKA"]["topic_purchases"]
    extra_configs['topic_restocks'] = config["KAFKA"]["topic_restocks"]


    # print("configs: {0}".format(str(configs)))

    return KafkaConfig(**extra_configs)
