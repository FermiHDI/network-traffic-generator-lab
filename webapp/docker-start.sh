#!/bin/sh
echo "Adding lab route"
ip route add $LAB_ROUTE via $LAB_ROUTE_VIA

echo "Starting Webapp via npm"
npm start $@
