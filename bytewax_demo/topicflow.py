from dotenv import load_dotenv
import os
from bytewax.connectors.kafka import operators as kop, KafkaSinkMessage, KafkaSink
from bytewax import operators as op
from bytewax.dataflow import Dataflow
import logging
from bytewax_demo.businesslogic import subtotals
from confluent_kafka import OFFSET_STORED
from bytewax.connectors.stdio import StdOutSink
import json
import dataclasses

logger = logging.getLogger(__name__)

load_dotenv()  # take environment variables from .env

print(
    f"""
{os.environ.get("BOOTSTRAP_SERVERS")}
{os.environ.get("INPUT_TOPIC")}
{os.environ.get("OUTPUT_TOPIC")}
{os.environ.get("COMMIT_INTERVAL_MS_CONFIG")}
"""
)

bootstrap_servers_csv = os.environ.get("BOOTSTRAP_SERVERS")
input_topic = os.environ.get("INPUT_TOPIC")
output_topic = os.environ.get("OUTPUT_TOPIC")

brokers = bootstrap_servers_csv.split(";") if bootstrap_servers_csv is not None else []

add_config = {
    "group.id": "consumer_group",
    "enable.auto.commit": "true",
    "auto.commit.interval.ms": os.environ.get("COMMIT_INTERVAL_MS_CONFIG"),
    "auto.offset.reset": "earliest",
}

flow = Dataflow("kstreams-kafka-demo2")

kinp = kop.input(
    "kafka-in",
    flow,
    starting_offset=OFFSET_STORED,
    add_config=add_config,
    brokers=brokers,
    batch_size=2,
    topics=[input_topic],
)


processed = op.map("map_kv", kinp.oks, lambda x: KafkaSinkMessage(x.key, x.value))
subtotal = op.map("map_sub_totals", processed, subtotals.make_subtotal)
keyed_subtotals = op.key_on("by_product_id", subtotal, lambda x: x.product_id)
running_totals = op.stateful_map("running_total", keyed_subtotals, subtotals.calc_running_total)
ready2go = op.map("map_sink", running_totals, lambda x: KafkaSinkMessage(x[0], json.dumps({'product': x[0], **dataclasses.asdict(x[1])})))
op.output("kafka-out", ready2go, KafkaSink(brokers, output_topic))