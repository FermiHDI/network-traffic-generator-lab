#!/usr/local/bin/python
# The shebang for the Standard Offical Python 3.12 docker image

from os import getenv
from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic, ConfigResource
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
      consumer = KafkaConsumer(bootstrap_servers=[input_bootstrap],
                               auto_offset_reset='earliest',
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
      producer = KafkaProducer(bootstrap_servers=[output_bootstrap])
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

  try:
    print(f"Updating topic retention")
    topic_list = []
    topic_list.append(ConfigResource(resource_type='TOPIC', name='ipflow_raw', configs={"retention.ms":"60000", "local.retention.ms":"60000"}))
    topic_list.append(ConfigResource(resource_type='TOPIC', name='ipflow', configs={"retention.ms":"60000", "local.retention.ms":"60000"}))
    admin_client.alter_configs(config_resources=topic_list)
  except Exception as e:
    print(f"Error: {e}")

  count = 0

  consumer.subscribe([input_topic])

  print(f"Input Topic {input_topic} Connected: {consumer.bootstrap_connected()}")
  print(f"Output Topic {output_topic} Connected: {producer.bootstrap_connected()}")
  print(f"Starting flow enrichment from {input_topic} and writing to {output_topic}")

  for message in consumer:
    rx_msg = loads(message.value.decode("utf-8"))

    port_num = 0
    if rx_msg["ip_proto"] == "tcp":
      port_num = 6
    elif rx_msg["ip_proto"] == "udp":
      port_num = 17

    timestamp = int(rx_msg["timestamp_start"].split(".")[0])

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
      "ip_proto": port_num,
      "tos": int(rx_msg["tos"]),
      "sampling_rate": int(rx_msg["sampling_rate"]),
      "packets": int(rx_msg["packets"]),
      "bytes": int(rx_msg["bytes"]),
      "timestamp": timestamp
    }

    producer.send(output_topic, value=dumps(tx_msg).encode("utf-8"))

    count += 1

    if count % 100000 == 0:
      print(f"Message {count} sent")
      print(f"Input Kafka Metrics: {consumer.metrics()}")
      print(f"Output Kafka Metrics: {producer.metrics()}")

  consumer.close()
  producer.close()
  print(f"Exiting with {count} messages sent")
