# backend/services/analytics_service.py
"""
Analytics Service for tracking metrics and events
"""

import os
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict

class AnalyticsService:
    """Service for analytics and metrics tracking"""
    
    def __init__(self):
        self.posthog = None
        self.metrics_cache = defaultdict(list)
        
        # Initialize PostHog if configured
        if os.getenv("POSTHOG_API_KEY"):
            try:
                from posthog import Posthog
                self.posthog = Posthog(
                    project_api_key=os.getenv("POSTHOG_API_KEY"),
                    host=os.getenv("POSTHOG_HOST", "https://eu.i.posthog.com")
                )
            except ImportError:
                print("PostHog not installed, analytics disabled")
    
    async def track_event(self, event_name: str, properties: Dict[str, Any] = None):
        """Track an analytics event"""
        # Store locally
        self.metrics_cache[event_name].append({
            "timestamp": datetime.now().isoformat(),
            "properties": properties or {}
        })
        
        # Send to PostHog if available
        if self.posthog:
            try:
                self.posthog.capture(
                    event_name,
                    properties=properties,
                    timestamp=datetime.now()
                )
            except Exception as e:
                print(f"PostHog tracking error: {e}")
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        from .queue_service import QueueService
        from .agent_service import AgentService
        
        queue_service = QueueService()
        agent_service = AgentService()
        
        # Initialize queue service
        await queue_service.initialize()
        
        # Get queue stats
        queue_stats = await queue_service.get_queue_stats()
        
        # Get agent stats
        agent_stats = await agent_service.get_performance_metrics()
        
        # Calculate event metrics
        event_metrics = self._calculate_event_metrics()
        
        # Cleanup
        await queue_service.cleanup()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "queues": queue_stats,
            "agents": agent_stats,
            "events": event_metrics,
            "system": {
                "uptime_seconds": self._get_uptime(),
                "memory_usage_mb": self._get_memory_usage(),
                "active_connections": self._get_active_connections()
            }
        }
    
    def _calculate_event_metrics(self) -> Dict[str, Any]:
        """Calculate metrics from cached events"""
        metrics = {
            "total_events": 0,
            "events_by_type": {},
            "events_last_hour": 0,
            "events_today": 0
        }
        
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        for event_type, events in self.metrics_cache.items():
            metrics["total_events"] += len(events)
            metrics["events_by_type"][event_type] = len(events)
            
            for event in events:
                event_time = datetime.fromisoformat(event["timestamp"])
                
                if event_time > hour_ago:
                    metrics["events_last_hour"] += 1
                
                if event_time > today_start:
                    metrics["events_today"] += 1
        
        return metrics
    
    def _get_uptime(self) -> int:
        """Get system uptime in seconds"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                return int(uptime_seconds)
        except:
            # Fallback for non-Linux systems
            return 0
    
    def _get_memory_usage(self) -> int:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss // 1024 // 1024
        except:
            return 0
    
    def _get_active_connections(self) -> int:
        """Get number of active WebSocket connections"""
        from ..api.websockets.email_stream import manager
        return len(manager.active_connections)
    
    async def generate_report(self, period: str = "daily") -> Dict[str, Any]:
        """Generate analytics report"""
        report = {
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "metrics": await self.get_metrics()
        }
        
        # Add period-specific calculations
        if period == "daily":
            report["summary"] = self._generate_daily_summary()
        elif period == "weekly":
            report["summary"] = self._generate_weekly_summary()
        
        return report
    
    def _generate_daily_summary(self) -> Dict[str, Any]:
        """Generate daily summary"""
        today = datetime.now().date()
        
        summary = {
            "date": today.isoformat(),
            "total_emails_processed": 0,
            "total_drafts_created": 0,
            "average_processing_time": 0,
            "error_rate": 0
        }
        
        # Calculate from cached events
        for event_type, events in self.metrics_cache.items():
            if event_type == "emails_fetched":
                for event in events:
                    event_date = datetime.fromisoformat(event["timestamp"]).date()
                    if event_date == today:
                        summary["total_emails_processed"] += event["properties"].get("count", 0)
            
            elif event_type == "draft_created":
                for event in events:
                    event_date = datetime.fromisoformat(event["timestamp"]).date()
                    if event_date == today:
                        summary["total_drafts_created"] += 1
        
        return summary
    
    def _generate_weekly_summary(self) -> Dict[str, Any]:
        """Generate weekly summary"""
        week_start = (datetime.now() - timedelta(days=7)).date()
        
        summary = {
            "week_start": week_start.isoformat(),
            "total_emails_processed": 0,
            "total_drafts_created": 0,
            "daily_breakdown": {}
        }
        
        # Calculate for each day of the week
        for i in range(7):
            day = week_start + timedelta(days=i)
            summary["daily_breakdown"][day.isoformat()] = {
                "emails": 0,
                "drafts": 0
            }
        
        # Populate from cached events
        for event_type, events in self.metrics_cache.items():
            for event in events:
                event_date = datetime.fromisoformat(event["timestamp"]).date()
                
                if week_start <= event_date <= datetime.now().date():
                    if event_type == "emails_fetched":
                        count = event["properties"].get("count", 0)
                        summary["total_emails_processed"] += count
                        if event_date.isoformat() in summary["daily_breakdown"]:
                            summary["daily_breakdown"][event_date.isoformat()]["emails"] += count
                    
                    elif event_type == "draft_created":
                        summary["total_drafts_created"] += 1
                        if event_date.isoformat() in summary["daily_breakdown"]:
                            summary["daily_breakdown"][event_date.isoformat()]["drafts"] += 1
        
        return summary