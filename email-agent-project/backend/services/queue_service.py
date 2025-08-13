# backend/services/queue_service.py
"""
Queue Service for managing email processing queues with Redis
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import redis.asyncio as redis
import os

class QueueService:
    """Service for managing processing queues"""
    
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client = None
        self.pubsub = None
    
    async def initialize(self):
        """Initialize Redis connection"""
        self.redis_client = await redis.from_url(self.redis_url, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
    
    async def check_health(self) -> str:
        """Check Redis health"""
        try:
            await self.redis_client.ping()
            return "healthy"
        except Exception as e:
            return f"unhealthy: {str(e)}"
    
    async def add_to_queue(self, queue_name: str, item: str):
        """Add item to processing queue"""
        queue_key = f"queue:{queue_name}"
        await self.redis_client.lpush(queue_key, item)
        
        # Publish event
        await self._publish_queue_event(queue_name, "item_added", {"item": item})
    
    async def get_from_queue(self, queue_name: str) -> Optional[str]:
        """Get item from processing queue"""
        queue_key = f"queue:{queue_name}"
        item = await self.redis_client.rpop(queue_key)
        
        if item:
            # Mark as processing
            processing_key = f"processing:{queue_name}"
            await self.redis_client.sadd(processing_key, item)
            
        return item
    
    async def mark_complete(self, queue_name: str, item: str):
        """Mark item as complete"""
        processing_key = f"processing:{queue_name}"
        await self.redis_client.srem(processing_key, item)
        
        # Add to completed set
        completed_key = f"completed:{queue_name}"
        await self.redis_client.sadd(completed_key, item)
        
        # Set expiry for completed items (7 days)
        await self.redis_client.expire(completed_key, 604800)
        
        # Publish event
        await self._publish_queue_event(queue_name, "item_completed", {"item": item})
    
    async def add_to_error_queue(self, queue_name: str, item: str, error: str):
        """Add failed item to error queue"""
        error_key = f"errors:{queue_name}"
        error_data = json.dumps({
            "item": item,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
        await self.redis_client.lpush(error_key, error_data)
        
        # Remove from processing
        processing_key = f"processing:{queue_name}"
        await self.redis_client.srem(processing_key, item)
    
    async def get_queue_stats(self) -> Dict:
        """Get queue statistics"""
        stats = {
            "total": 0,
            "processing": 0,
            "processed": 0,
            "errors": 0,
            "queues": {}
        }
        
        # Get all queue keys
        queue_keys = await self.redis_client.keys("queue:*")
        
        for key in queue_keys:
            queue_name = key.split(":")[1]
            queue_size = await self.redis_client.llen(key)
            processing_size = await self.redis_client.scard(f"processing:{queue_name}")
            completed_size = await self.redis_client.scard(f"completed:{queue_name}")
            error_size = await self.redis_client.llen(f"errors:{queue_name}")
            
            stats["queues"][queue_name] = {
                "pending": queue_size,
                "processing": processing_size,
                "completed": completed_size,
                "errors": error_size
            }
            
            stats["total"] += queue_size
            stats["processing"] += processing_size
            stats["processed"] += completed_size
            stats["errors"] += error_size
        
        return stats
    
    async def get_queued_emails(self) -> List[Dict]:
        """Get emails currently in queue"""
        emails = []
        
        # Get from categorize queue
        categorize_items = await self.redis_client.lrange("queue:categorize", 0, -1)
        for item in categorize_items:
            emails.append({"id": item, "status": "pending_categorization"})
        
        # Get from process queue
        process_items = await self.redis_client.lrange("queue:process", 0, -1)
        for item in process_items:
            emails.append({"id": item, "status": "pending_processing"})
        
        return emails
    
    async def clear_queue(self, queue_name: str):
        """Clear a specific queue"""
        queue_key = f"queue:{queue_name}"
        await self.redis_client.delete(queue_key)
        
        # Clear processing and errors
        await self.redis_client.delete(f"processing:{queue_name}")
        await self.redis_client.delete(f"errors:{queue_name}")
    
    async def subscribe_to_events(self, channel: str):
        """Subscribe to Redis pub/sub channel"""
        await self.pubsub.subscribe(channel)
        return self.pubsub
    
    async def _publish_queue_event(self, queue_name: str, event_type: str, data: Dict):
        """Publish queue event"""
        event = {
            "queue": queue_name,
            "event": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Publish to general channel
        await self.redis_client.publish("queue:events", json.dumps(event))
        
        # Publish to queue-specific channel
        await self.redis_client.publish(f"queue:{queue_name}:events", json.dumps(event))
    
    async def cleanup(self):
        """Cleanup Redis connections"""
        if self.pubsub:
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.close()