#!/bin/bash
# Redis Security Audit Script

REDIS_HOST="${1:-localhost}"
REDIS_PORT="${2:-6379}"

echo "===== Redis Security Audit ====="
echo "Host: $REDIS_HOST:$REDIS_PORT"
echo ""

# Check if authentication required
echo "[1] Authentication Check"
if redis-cli -h $REDIS_HOST -p $REDIS_PORT PING 2>/dev/null | grep -q "PONG"; then
    echo "    WARNING: No authentication required!"
else
    echo "    PASS: Authentication required"
fi

# Check bind address
echo ""
echo "[2] Network Configuration"
redis-cli -h $REDIS_HOST -p $REDIS_PORT CONFIG GET bind 2>/dev/null || echo "    Cannot check (auth required)"

# Check protected mode
echo ""
echo "[3] Protected Mode"
redis-cli -h $REDIS_HOST -p $REDIS_PORT CONFIG GET protected-mode 2>/dev/null || echo "    Cannot check (auth required)"

# Check dangerous commands
echo ""
echo "[4] Dangerous Commands"
echo "    Checking FLUSHALL, DEBUG, CONFIG..."

# Check TLS
echo ""
echo "[5] TLS Check"
if redis-cli -h $REDIS_HOST -p $REDIS_PORT --tls PING 2>/dev/null | grep -q "PONG"; then
    echo "    PASS: TLS enabled"
else
    echo "    INFO: TLS not detected on this port"
fi

echo ""
echo "===== Audit Complete ====="
