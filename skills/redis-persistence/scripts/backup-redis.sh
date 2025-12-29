#!/bin/bash
# Redis Backup Script with S3 upload support

set -e

REDIS_DIR="/var/lib/redis"
BACKUP_DIR="/var/backups/redis"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Trigger background save
echo "Triggering BGSAVE..."
redis-cli BGSAVE

# Wait for save to complete
while [ $(redis-cli LASTSAVE) == $(redis-cli LASTSAVE) ]; do
    sleep 1
done
sleep 2

# Copy RDB file
echo "Copying RDB file..."
cp "$REDIS_DIR/dump.rdb" "$BACKUP_DIR/dump_$DATE.rdb"

# Copy AOF if exists
if [ -f "$REDIS_DIR/appendonly.aof" ]; then
    echo "Copying AOF file..."
    cp "$REDIS_DIR/appendonly.aof" "$BACKUP_DIR/appendonly_$DATE.aof"
fi

# Compress
echo "Compressing..."
gzip "$BACKUP_DIR/dump_$DATE.rdb"
[ -f "$BACKUP_DIR/appendonly_$DATE.aof" ] && gzip "$BACKUP_DIR/appendonly_$DATE.aof"

# Optional: Upload to S3
# aws s3 cp "$BACKUP_DIR/dump_$DATE.rdb.gz" s3://bucket/redis-backups/

# Cleanup old backups
echo "Cleaning up old backups..."
find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup complete: dump_$DATE.rdb.gz"
