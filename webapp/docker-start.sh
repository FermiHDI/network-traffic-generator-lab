#!/bin/sh
echo "Adding test route"
ip route add 10.140.0.0/16 via 10.140.20.2

echo "Starting Webapp via npm"
npm start "$@"