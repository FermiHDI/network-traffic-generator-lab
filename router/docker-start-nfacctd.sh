#!/bin/sh

# Installing Kafka CLI
cd /tmp
curl -fsSLo kafka.tgz https://dlcdn.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
tar -xzf kafka.tgz
mv kafka_2.13-3.7.0 /opt/kafka

# Wait for Kafka To Fully Load
echo Pausing for 60 seconds for Kafka to fully load
sleep 60s
# Crate Kafka Topics
echo Creating Kafka Topics
/opt/kafka/bin/kafka-topics.sh --bootstrap-server $KAFKA_SERVER:9092 --create --topic ipflow --partitions 10 --replication-factor 1 --config cleanup.policy=delete --config compression.type=lz4 --config retention.ms=300000
/opt/kafka/bin/kafka-topics.sh --bootstrap-server $KAFKA_SERVER:9092 --create --topic iprouting --partitions 10 --replication-factor 1 --config cleanup.policy=delete --config compression.type=lz4 --config retention.ms=300000
/opt/kafka/bin/kafka-topics.sh --bootstrap-server $KAFKA_SERVER:9092 --create --topic nettelemetry --partitions 10 --replication-factor 1 --config cleanup.policy=delete --config compression.type=lz4 --config retention.ms=300000

# Start pmacct Netflow collector
echo Starting pmacct netflow collector
/usr/local/sbin/nfacctd -f /etc/pmacct/nfacctd.conf $@
sleep infinity
