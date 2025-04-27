from stream_generator.configuration_logic.traffic_generation.domain import modeling, exceptions

def traffic_configuration_data_testing(traffic_config: modeling.TrafficConfig) -> None:
    
    if(traffic_config.number_of_sales <= 0):
        raise exceptions.NonPositiveNumSalesException()

    if(traffic_config.min_sale_freq <= 0):
        raise exceptions.NonPositiveMinSaleFrequenceException()
    if(traffic_config.max_sale_freq <= 0):
        raise exceptions.NonPositiveMaxSaleFrequencyException()

    if(traffic_config.max_sale_freq < traffic_config.min_sale_freq):
        raise exceptions.MinMaxSaleFrequencyException()

    if len(traffic_config.transaction_items_weights) == 0:
        raise exceptions.EmptyTransactionItemsWeights()

    for weight in traffic_config.transaction_items_weights:
        if(weight <= 0):
            raise exceptions.NonPositiveTransactionItemsWeightException()