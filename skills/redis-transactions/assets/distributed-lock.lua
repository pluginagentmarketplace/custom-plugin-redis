-- Redis Distributed Lock (Redlock simplified)
-- EVALSHA <sha> 1 lock:resource owner_id ttl_ms

local key = KEYS[1]
local owner = ARGV[1]
local ttl = tonumber(ARGV[2])

-- Try to acquire lock
local acquired = redis.call('SET', key, owner, 'NX', 'PX', ttl)

if acquired then
    return {1, ttl}  -- Lock acquired
end

-- Check if we already own it
local current_owner = redis.call('GET', key)
if current_owner == owner then
    -- Extend lock
    redis.call('PEXPIRE', key, ttl)
    return {1, ttl}  -- Lock extended
end

-- Lock held by someone else
local remaining = redis.call('PTTL', key)
return {0, remaining}  -- Lock not acquired, return TTL
