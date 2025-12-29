---
description: Run Redis performance benchmarks and analyze results
allowed-tools: Read, Bash
---

# /redis-benchmark Command

Run comprehensive Redis performance benchmarks.

## Usage

```
/redis-benchmark [quick|standard|full]
```

## Benchmark Levels

### Quick (30 seconds)
- Basic SET/GET
- 10,000 operations
- Single connection

### Standard (2 minutes)
- All data types
- 100,000 operations
- Pipelining comparison

### Full (5 minutes)
- All operations
- 1,000,000 operations
- Multiple connection levels
- Latency percentiles

## What It Measures

1. **Throughput**
   - Operations per second
   - By command type

2. **Latency**
   - Average latency
   - P50, P99, P99.9 percentiles

3. **Pipelining Effect**
   - Without pipeline
   - With 16, 64, 256 pipeline

4. **Data Size Impact**
   - Small values (100B)
   - Medium values (1KB)
   - Large values (10KB)

## Example Output

```
Redis Benchmark Results
=======================
SET: 125,000 ops/sec (avg 0.8ms)
GET: 150,000 ops/sec (avg 0.6ms)

With Pipeline (16):
SET: 850,000 ops/sec
GET: 950,000 ops/sec

Latency Percentiles:
P50: 0.5ms
P99: 2.1ms
P99.9: 5.8ms
```
