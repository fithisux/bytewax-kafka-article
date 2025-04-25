from sales_generator import traffic_generator
from sales_generator.configuration_logic import kafkaparams

import dataclasses

import confluent_kafka.admin


def main():
    kafka_config = kafkaparams.configuration.get_config()

    ##
    ## from https://stackoverflow.com/questions/26021541/how-to-programmatically-create-a-topic-in-apache-kafka-using-python
    ##
    kafka_admin = confluent_kafka.admin.AdminClient(dataclasses.asdict(kafka_config))

    existing_topics = kafka_admin.list_topics().topics

    topics_to_delete = []

    if kafka_config.topic_products in existing_topics:
        topics_to_delete.append(kafka_config.topic_products)

    if kafka_config.topic_purchases in existing_topics:
        topics_to_delete.append(kafka_config.topic_purchases)

    if kafka_config.topic_inventories in existing_topics:
        topics_to_delete.append(kafka_config.topic_inventories)

    kafka_admin.delete_topics(topics_to_delete)

    new_topic_products = confluent_kafka.admin.NewTopic(
        kafka_config.topic_products, 1, 1
    )
    new_topic_purchases = confluent_kafka.admin.NewTopic(
        kafka_config.topic_purchases, 1, 1
    )
    new_topic_inventories = confluent_kafka.admin.NewTopic(
        kafka_config.topic_inventories, 1, 1
    )

    kafka_admin.create_topics(
        [new_topic_products, new_topic_purchases, new_topic_inventories]
    )

    traffic_generator.generate_traffic(kafka_config)


if __name__ == "__main__":
    main()
