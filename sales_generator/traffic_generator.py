from sales_generator.configuration_logic.data_generation import configuration
from sales_generator.configuration_logic.kafkaparams.configuration import KafkaConfig
from sales_generator.business_logic import sales_generation, deserializers
from kafka import KafkaProducer
import json
import dataclasses
import time
import random

def publish_to_kafka(topic, message, kafka_config: KafkaConfig):
    producer = KafkaProducer(
        value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
        **dataclasses.asdict(kafka_config.kafka_connection_config),
    )
    key = topic.split(".")[1]
    producer.send(topic, key=key.encode("utf-8"), value=message)
    print("Topic: {0}, Value: {1}".format(topic, message))


def generate_traffic(kafka_config: KafkaConfig):
    generator_config, traffic_config = configuration.get_config()

    products = deserializers.deserialize_product_list(
        generator_config.min_inventory
    )

    for product in products:
        print(f"Publishing {product}")
        publish_to_kafka(kafka_config.topic_products, product, kafka_config)

    for _ in range(0, traffic_config.number_of_sales):
        new_purchase, new_inventory = sales_generation.generate_sale(
            products, generator_config
        )
        if new_purchase is not None:
            print(f"Publishing {new_purchase}")
            publish_to_kafka(kafka_config.topic_purchases, new_purchase, kafka_config)
        if new_inventory is not None:
            print(f"Publishing {new_inventory}")
            publish_to_kafka(kafka_config.topic_inventories, new_inventory, kafka_config)

        time.sleep(random.randint(traffic_config.min_sale_freq, traffic_config.max_sale_freq))
