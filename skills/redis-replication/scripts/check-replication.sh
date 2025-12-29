#!/bin/bash
# Check Redis replication status

MASTER_HOST="${1:-localhost}"
MASTER_PORT="${2:-6379}"
PASSWORD="${3:-}"

AUTH=""
[ -n "$PASSWORD" ] && AUTH="-a $PASSWORD"

echo "===== Replication Status ====="
redis-cli -h "$MASTER_HOST" -p "$MASTER_PORT" $AUTH INFO replication

echo ""
echo "===== Replication Lag ====="
redis-cli -h "$MASTER_HOST" -p "$MASTER_PORT" $AUTH INFO replication | grep -E "(role|connected_slaves|master_repl_offset|slave.*offset)"
