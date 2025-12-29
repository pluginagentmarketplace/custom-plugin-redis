#!/bin/bash
# Redis Strings Benchmark Script

echo "===== Redis Strings Benchmark ====="
echo ""

# SET benchmark
echo "SET operations (100k):"
redis-benchmark -t set -n 100000 -q

# GET benchmark
echo "GET operations (100k):"
redis-benchmark -t get -n 100000 -q

# INCR benchmark
echo "INCR operations (100k):"
redis-benchmark -t incr -n 100000 -q

# MSET benchmark
echo "MSET operations (10k, 10 keys each):"
redis-benchmark -n 10000 -q mset key1 val1 key2 val2 key3 val3 key4 val4 key5 val5 key6 val6 key7 val7 key8 val8 key9 val9 key10 val10

echo ""
echo "===== Benchmark Complete ====="
