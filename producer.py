from sales_generator import traffic_generator

from configuration_logic import kafkaparams


if __name__ == "__main__":
    kafka_config = kafkaparams.configuration.get_config()
    traffic_generator.generate_traffic(kafka_config)