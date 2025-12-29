#!/bin/bash
# Test Redis Modules availability

HOST="${1:-localhost}"
PORT="${2:-6379}"

echo "===== Redis Modules Check ====="

echo ""
echo "[Loaded Modules]"
redis-cli -h $HOST -p $PORT MODULE LIST

echo ""
echo "[Testing RedisJSON]"
redis-cli -h $HOST -p $PORT JSON.SET test:json $ '{"test":true}' 2>/dev/null && echo "RedisJSON: Available" || echo "RedisJSON: Not loaded"
redis-cli -h $HOST -p $PORT DEL test:json 2>/dev/null

echo ""
echo "[Testing RediSearch]"
redis-cli -h $HOST -p $PORT FT._LIST 2>/dev/null && echo "RediSearch: Available" || echo "RediSearch: Not loaded"

echo ""
echo "[Testing RedisTimeSeries]"
redis-cli -h $HOST -p $PORT TS.INFO test:ts 2>/dev/null
echo "RedisTimeSeries: Check above for availability"

echo ""
echo "[Testing RedisBloom]"
redis-cli -h $HOST -p $PORT BF.INFO test:bf 2>/dev/null
echo "RedisBloom: Check above for availability"

echo ""
echo "===== Check Complete ====="
