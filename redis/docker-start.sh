#!/bin/sh
echo "Adding Test Routes"
ip route add 10.140.0.0/16 via 10.140.30.2

echo "Starting Redis"
redis-server $@
