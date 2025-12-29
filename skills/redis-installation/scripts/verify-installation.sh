#!/bin/bash
# Redis Installation Verification Script

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
log_fail() { echo -e "${RED}[FAIL]${NC} $1"; }
log_info() { echo -e "${YELLOW}[INFO]${NC} $1"; }

TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local name=$1
    local command=$2
    local expected=$3

    result=$(eval "$command" 2>/dev/null || echo "FAILED")

    if [[ "$result" == *"$expected"* ]]; then
        log_pass "$name"
        ((TESTS_PASSED++))
    else
        log_fail "$name (expected: $expected, got: $result)"
        ((TESTS_FAILED++))
    fi
}

echo "========================================"
echo "Redis Installation Verification"
echo "========================================"
echo ""

# Test 1: Redis CLI available
log_info "Checking Redis CLI..."
run_test "Redis CLI available" "which redis-cli" "redis-cli"

# Test 2: Redis server ping
log_info "Testing connection..."
run_test "Redis server responds to PING" "redis-cli PING" "PONG"

# Test 3: Redis version
log_info "Checking version..."
run_test "Redis version detected" "redis-cli INFO server | grep redis_version" "redis_version"

# Test 4: Basic SET/GET
log_info "Testing basic operations..."
redis-cli SET __verify_test__ "test_value" > /dev/null 2>&1
run_test "SET command works" "redis-cli GET __verify_test__" "test_value"
redis-cli DEL __verify_test__ > /dev/null 2>&1

# Test 5: Memory info
log_info "Checking memory..."
run_test "Memory stats available" "redis-cli INFO memory | grep used_memory_human" "used_memory_human"

# Test 6: Persistence check
log_info "Checking persistence..."
run_test "Persistence config available" "redis-cli CONFIG GET appendonly" "appendonly"

echo ""
echo "========================================"
echo "Verification Summary"
echo "========================================"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! Redis is properly installed.${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Please check your installation.${NC}"
    exit 1
fi
