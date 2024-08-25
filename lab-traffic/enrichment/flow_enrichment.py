#!/usr/local/bin/python
# The shebang for the Standard Offical Python 3.12 docker image

from os import getenv
from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from json import loads, dumps
from socket import inet_aton
from struct import unpack

from time import sleep, time

if __name__ == "__main__":
  input_topic = getenv("KAFKA_INPUT_TOPIC", "ipflow_raw")
  output_topic = getenv("KAFKA_OUTPUT_TOPIC", "ipflow")
  input_group = getenv("KAFKA_INPUT_GROUP", "to_enrich")
  output_group = getenv("KAFKA_INPUT_GROUP", "enriched")
  input_bootstrap_server = getenv("KAFKA_INPUT_BOOTSTRAP_SERVER", "kafka")
  output_bootstrap_server = getenv("KAFKA_OUTPUT_BOOTSTRAP_SERVER", "kafka")
  input_bootstrap_port = getenv("KAFKA_INPUT_BOOTSTRAP_PORT", "9092")
  output_bootstrap_port = getenv("KAFKA_OUTPUT_BOOTSTRAP_PORT", "9092")
  input_bootstrap = input_bootstrap_server + ":" + input_bootstrap_port
  output_bootstrap = output_bootstrap_server + ":" + output_bootstrap_port

  timeout = time() + 300  # 5 Mins
  while time() < timeout:
    print("Checking Kafka broker")
    connected = False
    # Check input kafka cluser for topic
    try:
      print(f"Checking if input topic {input_topic} exists")
      consumer = KafkaConsumer(input_topic,
                                group_id=input_group,
                                bootstrap_servers=[input_bootstrap],
                                consumer_timeout_ms=120000)
      existing_topics = consumer.topics()
      if input_topic not in existing_topics:
        print(f"Creating input topic {input_topic}")
        admin_client = KafkaAdminClient(bootstrap_servers=[input_bootstrap])
        new_topics = [NewTopic(name=input_topic, num_partitions=1, replication_factor=1)]
        admin_client.create_topics(new_topics=new_topics, validate_only=False)
      else:
        print(f"Input topic {input_topic} found")
      connected = True

      # Check output kafka cluser for topic
      print(f"Checking if output topic {output_topic} exists")
      consumer = KafkaConsumer(output_topic,
                                group_id=output_group,
                                bootstrap_servers=[output_bootstrap],
                                consumer_timeout_ms=120000)
      existing_topics = consumer.topics()
      if output_topic not in existing_topics:
        print(f"Creating output topic {output_topic}")
        admin_client = KafkaAdminClient(bootstrap_servers=[output_bootstrap])
        new_topics = [NewTopic(name=output_topic, num_partitions=1, replication_factor=1)]
        admin_client.create_topics(new_topics=new_topics, validate_only=False)
      else:
        print(f"Output topic {output_topic} found")
      connected = True
    except Exception as e:
      print(f"Error: {e}")
      connected = False

    if connected:
      break
    sleep (5)

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
