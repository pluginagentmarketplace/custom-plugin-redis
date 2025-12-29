#!/usr/bin/env python3
"""Redis Hash Migration Script - Migrate data between hash structures"""

import redis
import json
from typing import Dict, List, Optional

class HashMigrator:
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def migrate_hash(self, source_key: str, target_key: str,
                     field_mapping: Optional[Dict[str, str]] = None) -> bool:
        """Migrate hash with optional field renaming"""
        data = self.redis.hgetall(source_key)

        if not data:
            print(f"Source hash {source_key} is empty")
            return False

        if field_mapping:
            data = {field_mapping.get(k, k): v for k, v in data.items()}

        self.redis.hset(target_key, mapping=data)
        print(f"Migrated {len(data)} fields from {source_key} to {target_key}")
        return True

    def bulk_migrate(self, pattern: str, transform_key: callable) -> int:
        """Bulk migrate hashes matching pattern"""
        count = 0
        cursor = 0

        while True:
            cursor, keys = self.redis.scan(cursor, match=pattern, count=100)

            for key in keys:
                if self.redis.type(key) == 'hash':
                    new_key = transform_key(key)
                    self.migrate_hash(key, new_key)
                    count += 1

            if cursor == 0:
                break

        return count

    def add_field_to_all(self, pattern: str, field: str, value: str) -> int:
        """Add a field to all hashes matching pattern"""
        count = 0
        cursor = 0

        while True:
            cursor, keys = self.redis.scan(cursor, match=pattern, count=100)

            for key in keys:
                if self.redis.type(key) == 'hash':
                    self.redis.hset(key, field, value)
                    count += 1

            if cursor == 0:
                break

        return count

if __name__ == "__main__":
    migrator = HashMigrator()

    # Example: Rename field in all user hashes
    # migrator.bulk_migrate("user:*",
    #     lambda k: k,
    #     {"username": "name"})

    print("Migration complete")
