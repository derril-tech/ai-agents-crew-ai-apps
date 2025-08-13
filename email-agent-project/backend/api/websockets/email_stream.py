# backend/api/websockets/email_stream.py
"""
WebSocket handler for real-time email updates
"""

import json
import asyncio
from typing import Dict, Set
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect, Depends
from jose import JWTError, jwt

from ...services.queue_service import QueueService
from ...services.event_service import EventService

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_subscriptions: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and register WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_subscriptions[user_id] = {"emails", "drafts", "agents"}  # Default subscriptions
        
    def disconnect(self, user_id: str):
        """Remove WebSocket connection"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_subscriptions:
            del self.user_subscriptions[user_id]
    
    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to specific user"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending to {user_id}: {e}")
                self.disconnect(user_id)
    
    async def broadcast(self, message: dict, channel: str = "general"):
        """Broadcast message to all connections subscribed to channel"""
        disconnected = []
        for user_id, websocket in self.active_connections.items():
            if channel in self.user_subscriptions.get(user_id, set()):
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    print(f"Error broadcasting to {user_id}: {e}")
                    disconnected.append(user_id)
        
        # Clean up disconnected clients
        for user_id in disconnected:
            self.disconnect(user_id)


# Global connection manager
manager = ConnectionManager()

# Initialize services
queue_service = QueueService()
event_service = EventService()


async def get_user_from_token(token: str) -> str:
    """Extract user from JWT token"""
    try:
        from ..routes.auth import SECRET_KEY, ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real-time updates
    """
    user_id = None
    
    try:
        # Wait for authentication message
        auth_message = await websocket.receive_json()
        
        if auth_message.get("type") != "auth":
            await websocket.close(code=1008, reason="Authentication required")
            return
        
        # Verify token
        token = auth_message.get("token")
        user_id = await get_user_from_token(token)
        
        if not user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
        
        # Connect user
        await manager.connect(websocket, user_id)
        
        # Send connection confirmation
        await manager.send_personal_message({
            "type": "connected",
            "timestamp": datetime.now().isoformat(),
            "user": user_id,
            "message": "Connected to email stream"
        }, user_id)
        
        # Start listening for events
        asyncio.create_task(handle_redis_events(user_id))
        
        # Handle incoming messages
        while True:
            try:
                data = await websocket.receive_json()
                await handle_client_message(data, user_id)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, user_id)
            except Exception as e:
                print(f"WebSocket error for {user_id}: {e}")
                await manager.send_personal_message({
                    "type": "error",
                    "message": str(e)
                }, user_id)
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        if user_id:
            manager.disconnect(user_id)
            print(f"User {user_id} disconnected")


async def handle_client_message(data: dict, user_id: str):
    """
    Handle messages from WebSocket client
    """
    message_type = data.get("type")
    
    if message_type == "subscribe":
        # Subscribe to specific channels
        channels = data.get("channels", [])
        if user_id in manager.user_subscriptions:
            manager.user_subscriptions[user_id].update(channels)
        
        await manager.send_personal_message({
            "type": "subscribed",
            "channels": list(manager.user_subscriptions[user_id])
        }, user_id)
        
    elif message_type == "unsubscribe":
        # Unsubscribe from channels
        channels = data.get("channels", [])
        if user_id in manager.user_subscriptions:
            for channel in channels:
                manager.user_subscriptions[user_id].discard(channel)
        
        await manager.send_personal_message({
            "type": "unsubscribed",
            "channels": list(manager.user_subscriptions.get(user_id, set()))
        }, user_id)
        
    elif message_type == "ping":
        # Respond to ping
        await manager.send_personal_message({
            "type": "pong",
            "timestamp": datetime.now().isoformat()
        }, user_id)
        
    elif message_type == "get_status":
        # Send current status
        status = await get_current_status()
        await manager.send_personal_message({
            "type": "status",
            "data": status
        }, user_id)
    
    else:
        await manager.send_personal_message({
            "type": "error",
            "message": f"Unknown message type: {message_type}"
        }, user_id)


async def handle_redis_events(user_id: str):
    """
    Listen for Redis pub/sub events and forward to WebSocket
    """
    try:
        # Subscribe to user-specific Redis channel
        pubsub = await queue_service.subscribe_to_events(f"user:{user_id}")
        
        async for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    event_data = json.loads(message["data"])
                    
                    # Forward to WebSocket
                    await manager.send_personal_message({
                        "type": "event",
                        "event": event_data.get("event"),
                        "data": event_data.get("data"),
                        "timestamp": datetime.now().isoformat()
                    }, user_id)
                    
                except json.JSONDecodeError:
                    print(f"Invalid event data: {message['data']}")
                    
    except Exception as e:
        print(f"Redis event handler error for {user_id}: {e}")


async def get_current_status() -> dict:
    """
    Get current system status
    """
    from ...services.agent_service import AgentService
    agent_service = AgentService()
    
    queue_stats = await queue_service.get_queue_stats()
    agent_status = await agent_service.get_status()
    
    return {
        "queue": queue_stats,
        "agents": agent_status,
        "timestamp": datetime.now().isoformat()
    }


# Event broadcasting functions for use by other services
async def broadcast_email_event(event_type: str, data: dict):
    """Broadcast email-related events"""
    await manager.broadcast({
        "type": "email_event",
        "event": event_type,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }, channel="emails")


async def broadcast_draft_event(event_type: str, data: dict):
    """Broadcast draft-related events"""
    await manager.broadcast({
        "type": "draft_event",
        "event": event_type,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }, channel="drafts")


async def broadcast_agent_event(event_type: str, data: dict):
    """Broadcast agent-related events"""
    await manager.broadcast({
        "type": "agent_event",
        "event": event_type,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }, channel="agents")


async def send_user_notification(user_id: str, notification: dict):
    """Send notification to specific user"""
    await manager.send_personal_message({
        "type": "notification",
        "data": notification,
        "timestamp": datetime.now().isoformat()
    }, user_id)