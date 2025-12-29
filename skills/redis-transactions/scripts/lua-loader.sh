#!/bin/bash
# Load Lua scripts into Redis and get SHA

REDIS_CLI="redis-cli"
SCRIPTS_DIR="$(dirname "$0")/../assets"

load_script() {
    local file=$1
    local name=$(basename "$file" .lua)

    if [ -f "$file" ]; then
        sha=$($REDIS_CLI SCRIPT LOAD "$(cat "$file")")
        echo "$name: $sha"
    fi
}

echo "Loading Lua scripts..."
echo "========================"

for script in "$SCRIPTS_DIR"/*.lua; do
    load_script "$script"
done

echo "========================"
echo "Done! Use EVALSHA with the SHA values above."
