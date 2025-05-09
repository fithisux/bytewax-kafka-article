# Purpose: Consumes all messages from Kafka topic for testing purposes
# Author:  Gary A. Stafford
# Date: 2022-08-29
# Instructions: Modify the configuration.ini file to meet your requirements.
#               Select the topic to view the messages from.

import json
from kafka import KafkaConsumer
from stream_generator.configuration_logic.kafkaparams import configuration
import dataclasses


def main():
    # choose any or all topics
    kafka_config = configuration.get_config()

    topics = (
        kafka_config.topic_products,
        kafka_config.topic_purchases,
        kafka_config.topic_restocks,
    )

    consumer = KafkaConsumer(
        *topics,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        bootstrap_servers=kafka_config.kafka_connection_config.bootstrap_servers,
    )

    for message in consumer:
        print(message.value)


if __name__ == "__main__":
    main()
