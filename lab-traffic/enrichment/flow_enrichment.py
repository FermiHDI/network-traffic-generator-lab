#!/usr/local/bin/python
# The shebang for the Standard Official Python 3.12 docker image

import os
from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic, ConfigResource # type: ignore
from json import loads, dumps
from socket import inet_aton
from struct import unpack
import typing
import logging
import threading
import json
import sys
import signal

from time import sleep, time

stopProgram = threading.Event()
stopped = threading.Event()

class FibEntry (typing.TypedDict):
  mask: int
  network: int
  asn: int
  
def loggingSetup():
  """
  This function sets up a logger for the application. It configures the logger to output messages to the console,
  sets the log level based on the environment variable LOG_LEVEL, and includes a custom log format.

  Parameters:
  None

  Returns:
  log (logging.Logger): The configured logger instance.
  """
  log = logging.getLogger()
  LOGLEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
  log.setLevel(LOGLEVEL)
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    "%(asctime)s  [%(levelname)s] (%(module)s:%(funcName)s:%(lineno)d) %(message)s"  # pylint: disable=line-too-long
  )
  handler.setFormatter(formatter)
  log.addHandler(handler)
  if log.level < logging.WARNING:
    log.info(f"Logger level set to {log.level}")
  else:
    print(f"Logger level set to {log.level}")
  return log

def loadNetworks(file_path="networks.json") -> list[FibEntry]:
  log.info(f"Loading networks from {file_path}")
  fibish = []
  
  with open("networks.json", "r") as f:
    nets_ = loads(f.read())["networks"]
    nets = sorted(nets_, key=lambda x: x["mask"])
    
    for net in nets:
      # IPv4 Only
      m = 32 - net["mask"]
      mask = int('ffffffff', 16) >> m << m
      network = unpack("!L", inet_aton(str(net["network"])))[0]
      asn = net["as"]
  
      fibish.append({
        "mask": mask,
        "network": network,
        "asn": asn,
      })
  
  log.info(f"Loaded {len(fibish)} networks: {json.dumps(fibish, indent=2) if len(fibish) < 10 else 'Too many entries to display'}")
  
  return fibish

def setupKafka(bootstrap_servers: typing.Union[str,list[str]], topics: list[str] = None, consumer: bool = False) -> typing.Union[KafkaConsumer, KafkaProducer]:
  """
  This function sets up a Kafka producer or consumer based on the provided parameters.
  It handles the creation of the topic if it does not exist and updates the topic retention policy.

  Parameters:
  - bootstrap_servers (typing.Union[str,list[str]]): A string or list of strings representing the Kafka bootstrap servers.
  - topic (str): The name of the Kafka topic.
  - consumer (bool): A boolean indicating whether to setup a Kafka consumer (True) or producer (False).

  Returns:
  - KafkaProducer: A KafkaProducer instance if consumer is False.
  - KafkaConsumer: A KafkaConsumer instance if consumer is True.

  Raises:
  - ValueError: If bootstrap_servers is not a string or a list of strings.
  """
  if consumer:
    log.info(f"Setting up Kafka consumer connection with brokers: {bootstrap_servers}, topics: {topics}")
  else:
    log.info(f"Setting up Kafka producer connection with brokers: {bootstrap_servers}")
    
  timeout = time() + 300  # 5 Mins

  if isinstance(bootstrap_servers, str):
    bootstrap_servers = [bootstrap_servers]
  elif not isinstance(bootstrap_servers, list):
    raise ValueError("bootstrap_servers must be a string or a list of strings")

  while time() < timeout:
    try:
      if consumer:
        kafka_connection = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                                        group_id='to_enrich',
                                        auto_offset_reset='earliest',
                                        consumer_timeout_ms=1000,
                                        max_poll_interval_ms=600000,
                                        max_poll_records=5000)

        existing_topics = kafka_connection.topics()      
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

        for topic in topics:
          if topic not in existing_topics:
            log.info(f"Topic {topic} does not exist. Creating it")
            try:
              new_topics = [NewTopic(name=topic, num_partitions=1, replication_factor=1)]
              admin_client.create_topics(new_topics=new_topics, validate_only=False)
              log.info(f"Topic {topic} created successfully")
            except Exception as e:
              log.error(f"Failed to create topic {topic}: {str(e)}")
          else:
            log.info(f"Topic {topic} already exists, no need to create it")

          topic_list = []
          topic_config = {
            "cleanup.policy":"delete", 
            "retention.ms":"60000", 
            "local.retention.ms":"60000", 
            "retention.bytes":"100000000"
          }
          topic_list.append(ConfigResource(resource_type='TOPIC', name=topic, configs=topic_config))        
          log.info(f"Updating retention for Topic {topic} with new config: {json.dumps(topic_config, indent=2)}")
          admin_client.alter_configs(config_resources=topic_list)
      else:
        kafka_connection = KafkaProducer(bootstrap_servers=[output_bootstrap])
      break

    except Exception as e:
      log.error(f"Failed to setup Kafka producer: {str(e)}")
      sleep(5)  # Retry after 5 seconds
  return kafka_connection
    
def enrich(input_bootstrap:str, input_topic:str, output_bootstrap:str, output_topic:str, fibish:list[FibEntry]=[], report_every_n_message: int = 1000000) -> None:
  log.info(f"Starting flow enrichment loop for messages from Kafka topic {input_topic} to Kafka topic {output_topic}")
  kafka_rx = setupKafka(input_bootstrap, [input_topic, output_topic], True)
  kafka_tx = setupKafka(output_bootstrap)
  
  kafka_rx.subscribe([input_topic])
  
  count = 0
  commit_at = 100000
  commit_at = commit_at if commit_at <= report_every_n_message else report_every_n_message
  
  while not stopProgram.is_set():
    try:
      for rx_msg__ in kafka_rx:
        rx_msg = loads(rx_msg__.value.decode("utf-8"))
        port_num = 0
        if rx_msg["ip_proto"] == "tcp":
          port_num = 6
        elif rx_msg["ip_proto"] == "udp":
          port_num = 17

        # Fix Timestamp; In production you would change this to this systems timestamp for a trusted timestamp
        timestamp = int(rx_msg["timestamp_start"].split(".")[0])
        
        # Convert the IP Address string to a BigEden Integer and map ASN
        ip_src = unpack("!L", inet_aton(str(rx_msg["ip_src"])))[0]
        as_src = 0
        for net in fibish:
          if ip_src & net["mask"] ^ net["network"] == 0:
            as_src = net["asn"]
            break
          
        ip_dst = unpack("!L", inet_aton(str(rx_msg["ip_dst"])))[0]
        as_dst = 0
        for net in fibish:
          if ip_dst & net["mask"] ^ net["network"] == 0:
            as_dst = net["asn"]
            break

        # Build the new message
        tx_msg = {
          "peer_ip_src": unpack("!L", inet_aton(str(rx_msg["peer_ip_src"])))[0],
          "iface_in": int(rx_msg["iface_in"]),
          "iface_out": int(rx_msg["iface_out"]),
          "as_src": as_src,
          "as_dst": as_dst,
          "ip_src": ip_src,
          "ip_dst": ip_dst,
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

        kafka_tx.send(output_topic, value=dumps(tx_msg).encode("utf-8"))

        count += 1

        if count % commit_at == 0:
          kafka_rx.commit()          

        if count % report_every_n_message == 0:
          count = 0
          log.info(f"Input Kafka Metrics: {kafka_rx.metrics()}")
          log.info(f"Output Kafka Metrics: {kafka_tx.metrics()}")
    
    except StopIteration:
      if stopProgram.is_set():
        log.info(f"Stopping flow enrichment loop")
        break

  log.info(f"Closing Kafka connections")
  kafka_rx.close()
  kafka_tx.close()
  log.info(f"Kafka connections closed")
    
def signal_handler(sig, frame):
  """
  Handle the SIGINT signal (Ctrl+C) to gracefully stop all process.

  This function is called when a SIGINT signal is received. It sets a stop flag
  for all process and waits for it to finish processing before exiting.

  Parameters:
  sig (int): The signal number.
  frame (frame): Current stack frame.

  Returns:
  None

  Side effects:
  - Logs an info message about exiting.
  - Sets the stop flag.
  - Waits for up to 60 seconds for all processes to stop.
  - Exits the program with status code 0 if successful, or 1 if timeout occurs.
  """
  log.info('Exiting on Ctrl+C')
  stopProgram.set()  # Set the stop flag

  time_out = time() + 60 # 1 minute timeout
  while time() < time_out and not stopped.is_set():
    time.sleep(1) # Wait for the stop flag to be set

  if time() >= time_out:
    log.error("Timeout reached while waiting for all processes to stop")
    sys.exit(1)
  else:
    log.info("All processes stopped, exiting gracefully")
    sys.exit(0)

if __name__ == "__main__":
  log = loggingSetup()
  signal.signal(signal.SIGINT, signal_handler)  
  
  fibish = loadNetworks("networks.json")
  
  input_topic = os.getenv("KAFKA_INPUT_TOPIC", "ipflow_raw")
  output_topic = os.getenv("KAFKA_OUTPUT_TOPIC", "ipflow")
  input_bootstrap_server = os.getenv("KAFKA_INPUT_BOOTSTRAP_SERVER", "kafka")
  output_bootstrap_server = os.getenv("KAFKA_OUTPUT_BOOTSTRAP_SERVER", "kafka")
  input_bootstrap_port = os.getenv("KAFKA_INPUT_BOOTSTRAP_PORT", "9092")
  output_bootstrap_port = os.getenv("KAFKA_OUTPUT_BOOTSTRAP_PORT", "9092")
  input_bootstrap = input_bootstrap_server + ":" + input_bootstrap_port
  output_bootstrap = output_bootstrap_server + ":" + output_bootstrap_port
  
  # try:
  enrich(input_bootstrap, input_topic, output_bootstrap, output_topic, fibish)
  # except Exception as e:
  #   log.error(f"Error occurred while enriching flow data: {str(e)}")
  #   sys.exit(1)
