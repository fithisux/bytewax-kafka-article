from stream_generator.configuration_logic.traffic_generation import deserializers as tgconfig
from stream_generator.configuration_logic.kafkaparams.configuration import KafkaConfig
from stream_generator.business_logic import sales_generator, deserializers
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
    producer.send(topic, key=key.encode("utf-8"), value=dataclasses.asdict(message))
    print("Topic: {0}, Value: {1}".format(topic, message))


def generate_traffic(kafka_config: KafkaConfig):
    traffic_config = tgconfig.deserialize()

    products = deserializers.deserialize_product_list()

    for product in products:
        print(f"Publishing {product}")
        publish_to_kafka(kafka_config.topic_products, product, kafka_config)

    for _ in range(0, traffic_config.number_of_sales):
        items = sales_generator.generate_choice_from_weights(
            traffic_config.transaction_items_weights
        )
        sales = sales_generator.generate_sales(products, items)
        for sale in sales:
            new_purchase, new_restock = sale
            if new_purchase is not None:
                print(f"Publishing {new_purchase}")
                publish_to_kafka(
                    kafka_config.topic_purchases, new_purchase, kafka_config
                )
            if new_restock is not None:
                print(f"Publishing {new_restock}")
                publish_to_kafka(
                    kafka_config.topic_restocks, new_restock, kafka_config
                )

        time.sleep(
            random.randint(traffic_config.min_sale_freq, traffic_config.max_sale_freq)
        )
