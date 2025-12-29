#!/usr/bin/env python3
"""Redis Streams Processor with Consumer Groups"""

import redis
import json
import time
from typing import Callable, Optional

class StreamProcessor:
    def __init__(self, host='localhost', port=6379,
                 stream='events', group='processors', consumer='worker-1'):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.stream = f'stream:{stream}'
        self.group = group
        self.consumer = consumer
        self._ensure_group()

    def _ensure_group(self):
        try:
            self.redis.xgroup_create(self.stream, self.group, id='0', mkstream=True)
        except redis.ResponseError as e:
            if 'BUSYGROUP' not in str(e):
                raise

    def process(self, handler: Callable[[dict], bool], count: int = 10,
                block: int = 5000) -> None:
        """Process stream messages"""
        print(f"Processing {self.stream} as {self.consumer}...")

        while True:
            messages = self.redis.xreadgroup(
                self.group, self.consumer,
                {self.stream: '>'},
                count=count, block=block
            )

            if not messages:
                continue

            for stream_name, entries in messages:
                for msg_id, data in entries:
                    try:
                        if handler(data):
                            self.redis.xack(self.stream, self.group, msg_id)
                        else:
                            print(f"Handler returned False for {msg_id}")
                    except Exception as e:
                        print(f"Error processing {msg_id}: {e}")

def example_handler(data: dict) -> bool:
    print(f"Processing: {data}")
    return True

if __name__ == "__main__":
    processor = StreamProcessor()
    processor.process(example_handler)
