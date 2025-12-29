#!/bin/bash
# Redis Performance Check Script

HOST="${1:-localhost}"
PORT="${2:-6379}"
AUTH="${3:-}"

REDIS_CLI="redis-cli -h $HOST -p $PORT"
[ -n "$AUTH" ] && REDIS_CLI="$REDIS_CLI -a $AUTH"

echo "===== Redis Performance Check ====="
echo ""

echo "[Memory]"
$REDIS_CLI INFO memory | grep -E "(used_memory_human|maxmemory_human|mem_fragmentation_ratio)"

echo ""
echo "[Stats]"
$REDIS_CLI INFO stats | grep -E "(ops_per_sec|keyspace_hits|keyspace_misses|expired_keys|evicted_keys)"

echo ""
echo "[Slow Log (Last 5)]"
$REDIS_CLI SLOWLOG GET 5

echo ""
echo "[Memory Doctor]"
$REDIS_CLI MEMORY DOCTOR

echo ""
echo "[Latency]"
$REDIS_CLI --latency-history -i 1 | head -5

echo ""
echo "===== Check Complete ====="
