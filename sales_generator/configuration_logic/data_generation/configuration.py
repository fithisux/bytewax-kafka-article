from sales_generator.configuration_logic.data_generation import deserializers
from sales_generator.configuration_logic.data_generation.domain import modeling

from typing import Tuple

def get_config() -> Tuple[modeling.GeneratorConfig, modeling.TrafficConfig] :
    generator_config, traffic_config = deserializers.deserialize()
    deserializers.generator_configuration_data_testing(generator_config)
    deserializers.traffic_configuration_data_testing(traffic_config)
    return (generator_config, traffic_config)
 