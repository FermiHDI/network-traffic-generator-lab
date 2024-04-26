#!/bin/sh
echo "Adding lab route"
ip route add $1 via $2

echo "Starting Webapp via npm"
npm start $3
