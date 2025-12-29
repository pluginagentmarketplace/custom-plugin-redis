-- Redis Lua Script: Leaderboard Operations
-- Atomic update score and return new rank

-- Update score and get rank
-- EVALSHA <sha> 1 leaderboard:key player_id score_delta
local key = KEYS[1]
local player = ARGV[1]
local delta = tonumber(ARGV[2])

-- Increment score
local new_score = redis.call('ZINCRBY', key, delta, player)

-- Get new rank (0-indexed, reverse order for leaderboard)
local rank = redis.call('ZREVRANK', key, player)

-- Get total players
local total = redis.call('ZCARD', key)

return {new_score, rank, total}

-- Example usage:
-- EVALSHA <sha> 1 leaderboard:game1 player:123 50
-- Returns: [new_score, rank (0-indexed), total_players]
