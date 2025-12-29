#!/bin/bash
# Redis Cluster Health Check

NODE="${1:-127.0.0.1:7000}"
PASSWORD="${2:-}"

AUTH=""
[ -n "$PASSWORD" ] && AUTH="-a $PASSWORD"

echo "===== Cluster Info ====="
redis-cli -c -h ${NODE%:*} -p ${NODE#*:} $AUTH CLUSTER INFO

echo ""
echo "===== Cluster Nodes ====="
redis-cli -c -h ${NODE%:*} -p ${NODE#*:} $AUTH CLUSTER NODES

echo ""
echo "===== Slot Coverage ====="
redis-cli --cluster check $NODE $AUTH
