from stream_generator.configuration_logic.traffic_generation import deserializers
from stream_generator.configuration_logic.traffic_generation.domain import modeling

from typing import Tuple

def get_config() -> modeling.TrafficConfig :
    traffic_config = deserializers.deserialize()
    deserializers.traffic_configuration_data_testing(traffic_config)
    return traffic_config
 