#!/bin/sh
echo "Adding lab route"
ip route add $LAB_ROUTE via $LAB_ROUTE_VIA

echo "Starting Locust"
locust --config /usr/src/app/locust.conf $@
