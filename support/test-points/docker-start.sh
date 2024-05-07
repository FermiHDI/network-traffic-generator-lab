#!/bin/sh
echo "Adding lab routes"
ip route add $LAB_ROUTE via $LAB_ROUTE_VIA

echo " Going to sleep forever"
sleep infinity
