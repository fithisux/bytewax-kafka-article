# Purpose: Consumes all messages from Kafka topic for testing purposes
# Author:  Gary A. Stafford
# Date: 2022-08-29
# Instructions: Modify the configuration.ini file to meet your requirements.
#               Select the topic to view the messages from.

import json
from kafka import KafkaConsumer
from sales_generator.configuration_logic import kafkaparams
import dataclasses


def main():
    # choose any or all topics
    # topics = (topic_purchases)
    kafka_config = kafkaparams.configuration.get_config()

    topics = (
        kafka_config.topic_products,
        kafka_config.topic_purchases,
        kafka_config.topic_inventories,
    )

    consumer = KafkaConsumer(
        *topics,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        **dataclasses.asdict(kafka_config),
    )

    for message in consumer:
        print(message.value)


if __name__ == "__main__":
    main()
