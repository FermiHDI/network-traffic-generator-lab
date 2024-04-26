#!/bin/sh
echo "Adding Test Routes"
ip route add $1 via $2

echo "Starting Redis"
redis-server $3
