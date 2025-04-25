from configuration_logic.sales_generator.domain import deserializers, modeling
from typing import Tuple

def get_config() -> Tuple[modeling.GeneratorConfig, modeling.TrafficConfig] :
    generator_config, traffic_config = deserializers.deserialize()
    deserializers.generator_configuration_data_testing(generator_config)
    deserializers.traffic_configuration_data_testing(traffic_config)
    return (generator_config, traffic_config)
 