#!/bin/sh
echo "Adding lab routes"
ip route add $1 via $2

echo " Going to sleep forever"
sleep infinity
