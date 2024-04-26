#!/bin/sh
echo "Adding lab route"
ip route add $1 via $2

echo "Starting Locust"
locust --config /usr/src/app/locust.conf $3
