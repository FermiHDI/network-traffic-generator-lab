#!/bin/sh
echo "Adding Test Routes"
ip route add $LAB_ROUTE via $LAB_ROUTE_VIA

echo "Starting Redis"
redis-server $@
