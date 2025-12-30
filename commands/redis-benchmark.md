---
description: Run Redis performance benchmarks and analyze results
allowed-tools: Read, Bash
sasmp_version: "1.3.0"
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  level:
    type: string
    required: false
    default: "standard"
    enum: [quick, standard, full, custom]
  host:
    type: string
    required: false
    default: "localhost"
  port:
    type: integer
    required: false
    default: 6379
  clients:
    type: integer
    required: false
    default: 50
  requests:
    type: integer
    required: false
    default: 100000
  pipeline:
    type: integer
    required: false
    default: 1
  data_size:
    type: integer
    required: false
    default: 3
    description: "Data size in bytes"

# Thresholds
thresholds:
  ops_excellent: 100000
  ops_good: 50000
  ops_acceptable: 20000
  latency_excellent_ms: 1
  latency_good_ms: 5
  latency_acceptable_ms: 20
---

# /redis-benchmark Command

Run comprehensive Redis performance benchmarks with detailed analysis.

## Usage

```
/redis-benchmark [quick|standard|full|custom] [options]
```

## Benchmark Levels

### Quick (30 seconds)
Fast smoke test for basic performance validation.

```bash
redis-benchmark -h localhost -p 6379 \
    -t set,get \
    -n 10000 \
    -c 10 \
    -q
```

**Measures:**
- Basic SET/GET throughput
- Single connection latency
- Connection overhead

### Standard (2 minutes)
Balanced benchmark for regular performance testing.

```bash
redis-benchmark -h localhost -p 6379 \
    -t set,get,incr,lpush,rpush,lpop,rpop,sadd,hset,zadd,lrange,mset \
    -n 100000 \
    -c 50 \
    -d 100 \
    --csv
```

**Measures:**
- All common operations
- Pipelining comparison (1, 16, 64)
- Multiple data sizes
- Connection pool performance

### Full (5-10 minutes)
Comprehensive benchmark for capacity planning.

```bash
redis-benchmark -h localhost -p 6379 \
    -n 1000000 \
    -c 200 \
    -P 16 \
    --csv \
    --threads 4
```

**Measures:**
- Maximum throughput
- Latency percentiles (P50, P95, P99, P99.9)
- Various data sizes (100B, 1KB, 10KB)
- Multiple connection levels (10, 50, 100, 200)
- Pipeline depths (1, 16, 64, 256)

## Benchmark Script

```bash
#!/bin/bash
# redis-benchmark-suite.sh

HOST=${1:-localhost}
PORT=${2:-6379}
LEVEL=${3:-standard}

echo "=== Redis Benchmark Suite ==="
echo "Host: $HOST:$PORT"
echo "Level: $LEVEL"
echo "Started: $(date)"
echo ""

REDIS_BENCH="redis-benchmark -h $HOST -p $PORT"

case $LEVEL in
    quick)
        echo "Running quick benchmark..."
        $REDIS_BENCH -t set,get -n 10000 -c 10 -q
        ;;

    standard)
        echo "Running standard benchmark..."
        echo ""
        echo "=== Without Pipeline ==="
        $REDIS_BENCH -t set,get,incr,lpush,lpop,sadd,hset,zadd -n 100000 -c 50 -q

        echo ""
        echo "=== With Pipeline (16) ==="
        $REDIS_BENCH -t set,get -n 100000 -c 50 -P 16 -q

        echo ""
        echo "=== Data Size Comparison ==="
        for SIZE in 100 1000 10000; do
            echo "Size: ${SIZE} bytes"
            $REDIS_BENCH -t set,get -n 50000 -c 50 -d $SIZE -q
        done
        ;;

    full)
        echo "Running full benchmark (this may take several minutes)..."

        # Create results directory
        RESULTS_DIR="benchmark_results_$(date +%Y%m%d_%H%M%S)"
        mkdir -p $RESULTS_DIR

        echo ""
        echo "=== Baseline (no pipeline) ==="
        $REDIS_BENCH -n 1000000 -c 50 --csv > $RESULTS_DIR/baseline.csv
        cat $RESULTS_DIR/baseline.csv | column -t -s,

        echo ""
        echo "=== Connection Scaling ==="
        for CLIENTS in 10 50 100 200; do
            echo "Clients: $CLIENTS"
            $REDIS_BENCH -t set,get -n 100000 -c $CLIENTS -q
        done > $RESULTS_DIR/connection_scaling.txt

        echo ""
        echo "=== Pipeline Scaling ==="
        for PIPELINE in 1 16 64 256; do
            echo "Pipeline: $PIPELINE"
            $REDIS_BENCH -t set,get -n 100000 -c 50 -P $PIPELINE -q
        done > $RESULTS_DIR/pipeline_scaling.txt

        echo ""
        echo "=== Latency Distribution ==="
        $REDIS_BENCH -t set,get -n 100000 -c 50 --latency > $RESULTS_DIR/latency.txt

        echo ""
        echo "Results saved to: $RESULTS_DIR/"
        ;;

    custom)
        echo "Custom benchmark mode - provide parameters"
        ;;
esac

echo ""
echo "Completed: $(date)"
```

## What It Measures

### 1. Throughput
Operations per second by command type.

| Command | Expected (standalone) | Expected (cluster) |
|---------|----------------------|-------------------|
| SET | 100K+ ops/s | 200K+ ops/s |
| GET | 120K+ ops/s | 250K+ ops/s |
| INCR | 100K+ ops/s | 200K+ ops/s |
| LPUSH | 100K+ ops/s | 200K+ ops/s |
| HSET | 100K+ ops/s | 200K+ ops/s |
| ZADD | 80K+ ops/s | 150K+ ops/s |

### 2. Latency Percentiles

| Percentile | Excellent | Good | Acceptable | Poor |
|------------|-----------|------|------------|------|
| P50 | <0.5ms | <1ms | <5ms | >5ms |
| P95 | <1ms | <5ms | <10ms | >10ms |
| P99 | <2ms | <10ms | <20ms | >20ms |
| P99.9 | <5ms | <20ms | <50ms | >50ms |

### 3. Pipelining Effect

```
Without Pipeline:
SET: 100,000 ops/sec
GET: 120,000 ops/sec

With Pipeline (16):
SET: 800,000 ops/sec (+700%)
GET: 950,000 ops/sec (+691%)

With Pipeline (64):
SET: 1,200,000 ops/sec (+1100%)
GET: 1,400,000 ops/sec (+1066%)
```

### 4. Data Size Impact

| Size | SET ops/s | GET ops/s | Notes |
|------|-----------|-----------|-------|
| 100B | 120K | 140K | Optimal |
| 1KB | 100K | 110K | Good |
| 10KB | 50K | 60K | Network bound |
| 100KB | 10K | 12K | Consider compression |

## Example Output

```
=== Redis Benchmark Results ===
Host: redis.example.com:6379
Level: standard
Date: 2025-01-15 10:30:00 UTC

Server Info:
  Version: 7.2.4
  Mode: Standalone
  Memory: 2.5GB / 4GB

Baseline Performance (50 clients, no pipeline):
--------------------------------------------------
Command     | Requests/s | Avg Latency | P99 Latency
------------|------------|-------------|------------
SET         | 125,432    | 0.39ms      | 1.2ms
GET         | 148,721    | 0.33ms      | 0.9ms
INCR        | 142,857    | 0.35ms      | 1.0ms
LPUSH       | 131,926    | 0.37ms      | 1.1ms
LPOP        | 134,228    | 0.36ms      | 1.1ms
HSET        | 118,343    | 0.42ms      | 1.3ms
ZADD        | 98,765     | 0.51ms      | 1.8ms
LRANGE_100  | 45,678     | 1.09ms      | 3.2ms
MSET (10)   | 78,125     | 0.64ms      | 2.1ms

Pipeline Performance (50 clients, pipeline=16):
--------------------------------------------------
Command     | Requests/s | Improvement
------------|------------|------------
SET         | 892,857    | +612%
GET         | 1,041,667  | +600%

Data Size Impact:
--------------------------------------------------
Size    | SET ops/s | GET ops/s
--------|-----------|----------
100B    | 125,432   | 148,721
1KB     | 98,765    | 112,359
10KB    | 45,678    | 52,631

Latency Distribution (GET):
--------------------------------------------------
Percentile | Latency
-----------|--------
P50        | 0.28ms
P95        | 0.72ms
P99        | 1.12ms
P99.9      | 2.45ms

Assessment: EXCELLENT
- Throughput exceeds baseline expectations
- Latency within acceptable bounds
- Pipeline scaling working correctly
```

## Comparison with Baseline

```bash
# Compare with previous run
/redis-benchmark full --compare baseline_20250114.csv
```

Output:
```
Performance Comparison
======================
                  Previous    Current     Change
SET ops/s         120,000     125,432     +4.5%
GET ops/s         145,000     148,721     +2.6%
P99 latency       1.5ms       1.2ms       -20%

Status: IMPROVED
```

## Troubleshooting

### Low Throughput
```
Issue: SET only achieving 20K ops/s

Diagnostics:
- Check network latency: redis-cli --latency
- Check slow log: SLOWLOG GET 10
- Check max clients: CONFIG GET maxclients

Possible fixes:
- Use pipelining
- Check for network bottlenecks
- Verify no persistence issues
```

### High Latency
```
Issue: P99 latency >50ms

Diagnostics:
- SLOWLOG GET 10
- CLIENT LIST (check blocked clients)
- INFO persistence (check AOF fsync)

Possible fixes:
- appendfsync everysec (not always)
- Disable THP
- Check for swap usage
```

### Inconsistent Results
```
Issue: High variance between runs

Diagnostics:
- Check background operations (BGSAVE)
- Check replication sync
- Monitor CPU usage

Possible fixes:
- Run benchmarks during quiet periods
- Disable BGSAVE during benchmark
- Use dedicated benchmark client
```

## Error Codes

| Code | Description | Action |
|------|-------------|--------|
| BM001 | Connection failed | Check host/port |
| BM002 | Auth required | Provide password |
| BM003 | Timeout | Increase timeout |
| BM004 | Memory limit | Reduce request count |
