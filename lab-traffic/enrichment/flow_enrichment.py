#!/usr/bin/env python

from os import getenv
from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
from json import loads, dumps
from socket import inet_aton
from struct import unpack

if __name__ == "__main__":
  input_topic = getenv("KAFKA_INPUT_TOPIC", "ipflow_raw")
  output_topic = getenv("KAFKA_OUTPUT_TOPIC", "ipflow")
  input_group = getenv("KAFKA_INPUT_GROUP", "to_enrich")
  input_bootstrap_server = getenv("KAFKA_INPUT_BOOTSTRAP_SERVER", "kafka")
  output_bootstrap_server = getenv("KAFKA_OUTPUT_BOOTSTRAP_SERVER", "kafka")
  input_bootstrap_port = getenv("KAFKA_INPUT_BOOTSTRAP_PORT", "9092")
  output_bootstrap_port = getenv("KAFKA_OUTPUT_BOOTSTRAP_PORT", "9092")
  input_bootstrap = input_bootstrap_server + ":" + input_bootstrap_port
  output_bootstrap = output_bootstrap_server + ":" + output_bootstrap_port

  # Check input kafka cluser for topic
  client = KafkaAdminClient(bootstrap_servers=input_bootstrap)
  topics = client.topic_partitions
  print(f"Checking if input topic {input_topic} exists")
  if input_topic not in topics:
    print(f"Input topic {input_topic} not foud, creating it")
    client.create_topics(new_topics=[input_topic], timeout_ms=5000)
  else:
    print(f"Input topic {input_topic} found")

  # Check output kafka cluser for topic
  client = KafkaAdminClient(bootstrap_servers=output_bootstrap)
  topics = client.topic_partitions
  print(f"Checking if output topic {output_topic} exists")
  if output_topic not in topics:
    print(f"Output topic {output_topic} not foud, creating it")
    client.create_topics(new_topics=[output_topic], timeout_ms=5000)
  else:
    print(f"Output topic {output_topic} found")

  producer = KafkaProducer(bootstrap_servers=[output_bootstrap])
  consumer = KafkaConsumer(input_topic,
                            group_id=input_group,
                            bootstrap_servers=[input_bootstrap],
                            consumer_timeout_ms=120000)
  
  count = 0

  print(f"Starting flow enrichment from {input_topic} and writing to {output_topic}")

  for message in consumer:
    rx_msg = loads(message.value.decode("utf-8"))

    tx_msg = {
      "peer_ip_src": unpack("!L", inet_aton(str(rx_msg["peer_ip_src"])))[0],
      "iface_in": int(rx_msg["iface_in"]),
      "iface_out": int(rx_msg["iface_out"]),
      "as_src": int(rx_msg["as_src"]),
      "as_dst": int(rx_msg["as_dst"]),
      "ip_src": unpack("!L", inet_aton(str(rx_msg["ip_src"])))[0],
      "ip_dst": unpack("!L", inet_aton(str(rx_msg["ip_dst"])))[0],
      "port_src": int(rx_msg["port_src"]),
      "port_dst": int(rx_msg["port_dst"]),
      "tcp_flags": int(rx_msg["tcp_flags"]),
      "ip_proto": int(rx_msg["ip_proto"]),
      "tos": int(rx_msg["tos"]),
      "sampling_rate": int(rx_msg["sampling_rate"]),
      "packets": int(rx_msg["packets"]),
      "bytes": int(rx_msg["bytes"]),
      "timestamp": int(rx_msg["timestamp_start"])
    }

    producer.send(output_topic, value=dumps(tx_msg).encode("utf-8"))

    count += 1

    if count % 10 == 0:
      print(f"Message {count} sent")
  
  print(f"Exiting with {count} messages sent")
