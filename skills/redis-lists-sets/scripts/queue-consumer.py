#!/usr/bin/env python3
"""Redis Queue Consumer Example"""

import redis
import json
import signal
import sys
from typing import Optional, Callable

class RedisQueueConsumer:
    def __init__(self, host: str = 'localhost', port: int = 6379,
                 queue_name: str = 'tasks', timeout: int = 30):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.queue_key = f'queue:{queue_name}'
        self.dlq_key = f'dlq:{queue_name}'
        self.timeout = timeout
        self.running = True

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        print("\nShutting down consumer...")
        self.running = False

    def consume(self, handler: Callable[[dict], bool]) -> None:
        """Consume messages from queue"""
        print(f"Consuming from {self.queue_key}...")

        while self.running:
            result = self.redis.blpop(self.queue_key, timeout=self.timeout)

            if result is None:
                continue

            _, message = result
            try:
                data = json.loads(message)
                success = handler(data)

                if not success:
                    self._send_to_dlq(message)

            except json.JSONDecodeError:
                print(f"Invalid JSON: {message}")
                self._send_to_dlq(message)
            except Exception as e:
                print(f"Error processing: {e}")
                self._send_to_dlq(message)

    def _send_to_dlq(self, message: str) -> None:
        """Send failed message to dead letter queue"""
        self.redis.rpush(self.dlq_key, message)
        print(f"Sent to DLQ: {message[:50]}...")

def example_handler(data: dict) -> bool:
    """Example message handler"""
    print(f"Processing: {data}")
    return True

if __name__ == "__main__":
    consumer = RedisQueueConsumer()
    consumer.consume(example_handler)
