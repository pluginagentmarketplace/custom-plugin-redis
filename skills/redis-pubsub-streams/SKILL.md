---
name: redis-pubsub-streams
description: Pub/Sub messaging for real-time communication and Streams for event logs, event sourcing, and consumer groups.
---

# Redis Pub/Sub & Streams

Real-time messaging and event processing.

## Pub/Sub Messaging

Simple publish-subscribe pattern.

```python
import redis
import threading

def subscriber():
    """Listen for messages"""
    r = redis.Redis()
    pubsub = r.pubsub()

    # Subscribe to channels
    pubsub.subscribe('news', 'alerts', 'updates')

    # Pattern-based subscription
    pubsub.psubscribe('user:*:notifications')

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Channel: {message['channel']}")
            print(f"Data: {message['data']}")

def publisher():
    """Send messages"""
    r = redis.Redis()

    # Publish
    subscribers = r.publish('news', 'Breaking news!')
    print(f"Reached {subscribers} subscribers")

    # Different channels
    r.publish('alerts', 'System alert')
    r.publish('user:123:notifications', 'New message')

# Run in separate threads
threading.Thread(target=subscriber, daemon=True).start()
threading.Thread(target=publisher, daemon=True).start()
```

### Pattern-Based Subscriptions

```python
pubsub = r.pubsub()

# Subscribe to patterns
pubsub.psubscribe('user:*:online')      # Any user online event
pubsub.psubscribe('notification:*')     # Any notification
pubsub.psubscribe('alert:*:critical')   # Critical alerts

for message in pubsub.listen():
    if message['type'] == 'pmessage':
        pattern = message['pattern']  # The pattern that matched
        channel = message['channel']  # The actual channel
        data = message['data']        # The message
        print(f"Pattern {pattern} matched: {channel} = {data}")
```

## Pub/Sub Use Cases

### Real-Time Notifications

```python
class NotificationService:
    def __init__(self):
        self.r = redis.Redis()

    def notify_user(self, user_id, notification):
        """Send notification to specific user"""
        channel = f'user:{user_id}:notifications'
        self.r.publish(channel, json.dumps(notification))

    def notify_all(self, notification):
        """Broadcast to all users"""
        self.r.publish('broadcast', json.dumps(notification))

    def subscribe_to_user(self, user_id, callback):
        """Subscribe to user notifications"""
        pubsub = self.r.pubsub()
        pubsub.subscribe(f'user:{user_id}:notifications')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                callback(data)

# Usage
service = NotificationService()

# Send notification
service.notify_user(123, {'type': 'message', 'text': 'Hi there!'})

# Listen for notifications
def handle_notification(notif):
    print(f"Got: {notif}")

service.subscribe_to_user(123, handle_notification)
```

### Real-Time Chat

```python
class ChatRoom:
    def __init__(self, room_name):
        self.room = f'chat:{room_name}'
        self.r = redis.Redis()

    def send_message(self, user, message):
        """Send message to chat room"""
        msg_obj = {
            'user': user,
            'text': message,
            'timestamp': str(datetime.now())
        }
        self.r.publish(self.room, json.dumps(msg_obj))

    def listen_messages(self, callback):
        """Listen for chat messages"""
        pubsub = self.r.pubsub()
        pubsub.subscribe(self.room)

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                callback(data)

# Usage
room = ChatRoom('general')

# Send message
room.send_message('Alice', 'Hello everyone!')

# Listen
def on_message(msg):
    print(f"{msg['user']}: {msg['text']}")

room.listen_messages(on_message)
```

## Streams (Advanced)

Event logs with consumer groups.

```python
# Add to stream
stream_id = r.xadd('events', {
    'user_id': '123',
    'action': 'login',
    'ip': '192.168.1.1'
})
# Returns: b'1609459200000-0' (timestamp-sequence)

# Read all
events = r.xrange('events')  # All from start
recent = r.xrevrange('events', count=10)  # Last 10

# Read range
range_events = r.xrange('events', min='1609459200000-0', max='1609459300000-0')

# Read specific time
time_events = r.xread({'events': '1609459200000'})
```

### Consumer Groups

Process stream messages reliably.

```python
# Setup consumer group
r.xgroup_create('orders', 'fulfillment_group', id='0')

# Consumer reads from group
messages = r.xreadgroup(
    groupname='fulfillment_group',
    consumername='worker1',
    streams={'orders': '>'},  # > = new messages
    count=1,
    block=0
)

# Process message
for stream, messages_list in messages:
    for msg_id, msg_data in messages_list:
        order = msg_data
        print(f"Processing order: {order}")

        # Acknowledge after processing
        r.xack('orders', 'fulfillment_group', msg_id)

# Get pending messages
pending = r.xpending('orders', 'fulfillment_group')
```

### Stream Example: Event Sourcing

```python
class EventStore:
    def __init__(self):
        self.r = redis.Redis()
        self.stream = 'events'

    def append_event(self, aggregate_id, event_type, data):
        """Record event"""
        event = {
            'aggregate_id': aggregate_id,
            'type': event_type,
            'timestamp': str(datetime.now()),
            'data': json.dumps(data)
        }
        return self.r.xadd(self.stream, event)

    def get_events(self, aggregate_id):
        """Get all events for aggregate"""
        events = self.r.xrange(self.stream)
        return [
            msg for msg_id, msg in events
            if msg[b'aggregate_id'].decode() == str(aggregate_id)
        ]

    def replay_events(self, aggregate_id):
        """Rebuild aggregate state from events"""
        state = {}
        for msg_id, msg in self.get_events(aggregate_id):
            event_type = msg[b'type'].decode()
            data = json.loads(msg[b'data'])

            # Apply event to state
            if event_type == 'user_created':
                state['name'] = data['name']
                state['email'] = data['email']
            elif event_type == 'email_changed':
                state['email'] = data['new_email']

        return state

# Usage
store = EventStore()

# Record events
store.append_event(123, 'user_created', {'name': 'Alice', 'email': 'alice@ex.com'})
store.append_event(123, 'email_changed', {'new_email': 'alice.new@ex.com'})

# Rebuild state
state = store.replay_events(123)
print(state)  # {'name': 'Alice', 'email': 'alice.new@ex.com'}
```

## Pub/Sub vs Streams

| Feature | Pub/Sub | Streams |
|---------|---------|---------|
| Persistence | No | Yes |
| History | No | Yes |
| Consumer Groups | No | Yes |
| Reliability | Fire-and-forget | Guaranteed delivery |
| Use Case | Real-time notifications | Event logs |
| Latency | Ultra-low | Very low |
| Scalability | Many subscribers | Many consumers |

## When to Use What

**Use Pub/Sub for**:
- Real-time chat
- Live notifications
- Broadcast messaging
- WebSocket communication
- Stock price updates
- Live sports scores

**Use Streams for**:
- Event sourcing
- Event logs
- Message queues with persistence
- Activity feeds
- Analytics events
- Audit trails

## Best Practices

### Pub/Sub
- ✅ Use pattern subscriptions for flexibility
- ✅ Handle reconnection gracefully
- ✅ Monitor subscriber count
- ❌ Don't rely on delivery (not persistent)
- ❌ Don't use for critical messages

### Streams
- ✅ Always use consumer groups for reliability
- ✅ Acknowledge messages after processing
- ✅ Monitor pending messages
- ✅ Set maxlen to prevent unbounded growth
- ❌ Don't ignore dead-letter handling

## Advanced Patterns

### Dead-Letter Queue (DLQ)

```python
def process_with_dlq(stream, group, consumer, max_retries=3):
    messages = r.xreadgroup(
        groupname=group,
        consumername=consumer,
        streams={stream: '>'},
        count=1
    )

    for stream_key, msgs in messages:
        for msg_id, data in msgs:
            try:
                process_message(data)
                r.xack(stream, group, msg_id)
            except Exception as e:
                # Check retry count
                info = r.xinfo_consumers(stream, group)
                if info[consumer]['pending'] > max_retries:
                    # Move to DLQ
                    r.xadd('dlq', data)
                    r.xack(stream, group, msg_id)
```

## Performance Tips

- Pub/Sub: <1ms latency, 100k+ subscribers
- Streams: <5ms latency, append only (fast writes)
- Consumer Groups: Enable parallel processing
- Trim streams: `XTRIM key MAXLEN 1000000`
- Monitor lag: Check pending count
