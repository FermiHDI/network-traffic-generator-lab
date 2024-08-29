#!/bin/bash

TIMEOUT=${TOMEOUT:=60}
LOOP_COUNT=0

while (( $LOOP_COUNT < $TIMEOUT ));
do
  echo "Trying to create the Kafka topic ${TOPIC} on broker ${BROKER}"
  /bin/kafka-topics --bootstrap-server ${BROKER} --if-not-exists --create --partitions ${PARTITIONS} --topic ${TOPIC}
  if [[ $? == 0 ]]; then
    echo "Done"
    exit 0
  fi
  echo "Could not create topic, will try again"
  ((LOOP_COUNT++))
  sleep 1
done
exit 1
