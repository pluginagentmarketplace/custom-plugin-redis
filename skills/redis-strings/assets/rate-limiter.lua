-- Redis Lua Script: Sliding Window Rate Limiter
-- Usage: EVALSHA <sha> 1 <key> <limit> <window_seconds>

local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local current = redis.call('GET', key)

if current == false then
    -- First request
    redis.call('SET', key, 1, 'EX', window)
    return {1, limit - 1, window}
end

local count = tonumber(current)

if count >= limit then
    -- Rate limit exceeded
    local ttl = redis.call('TTL', key)
    return {0, 0, ttl}
end

-- Increment counter
redis.call('INCR', key)
return {1, limit - count - 1, redis.call('TTL', key)}

-- Return format: {allowed (1/0), remaining, reset_in_seconds}
