# backend/services/agent_service.py
"""
Agent Service for managing CrewAI agents
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import os

from ..agents.flows.email_flow import EmailProcessingFlow
from ..database.connection import SessionLocal
from ..models.agent import AgentLog
from .queue_service import QueueService
from ..api.websockets.email_stream import broadcast_agent_event

class AgentService:
    """Service for managing email processing agents"""
    
    def __init__(self):
        self.flow = None
        self.is_running_flag = False
        self.start_time = None
        self.stats = {
            "emails_processed": 0,
            "drafts_created": 0,
            "errors": 0,
            "last_check": None
        }
        self.current_task = None
        self.queue_service = QueueService()
    
    def is_running(self) -> bool:
        """Check if agent is currently running"""
        return self.is_running_flag
    
    async def start_processing(self, config: Dict[str, Any]):
        """Start the agent processing flow"""
        if self.is_running_flag:
            return
        
        self.is_running_flag = True
        self.start_time = datetime.now()
        self.flow = EmailProcessingFlow()
        
        # Configure flow
        self.flow.check_interval = config.get("interval", 180)
        self.flow.batch_size = config.get("batch_size", 10)
        
        try:
            # Broadcast start event
            await broadcast_agent_event("started", {
                "config": config,
                "timestamp": self.start_time.isoformat()
            })
            
            # Start the flow
            await self.flow.start()
            
        except Exception as e:
            print(f"Agent processing error: {e}")
            self.stats["errors"] += 1
            await self._log_error("flow_error", str(e))
        finally:
            self.is_running_flag = False
            await broadcast_agent_event("stopped", {
                "runtime_seconds": (datetime.now() - self.start_time).total_seconds(),
                "stats": self.stats
            })
    
    async def stop_processing(self):
        """Stop the agent processing flow"""
        if self.flow:
            self.flow.stop()
        self.is_running_flag = False
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        status = {
            "is_running": self.is_running_flag,
            "status": "running" if self.is_running_flag else "idle",
            "current_task": self.current_task,
            "started_at": self.start_time.isoformat() if self.start_time else None,
            "last_check": self.stats["last_check"],
            "emails_processed": self.stats["emails_processed"],
            "drafts_created": self.stats["drafts_created"],
            "error_count": self.stats["errors"]
        }
        
        if self.is_running_flag and self.start_time:
            status["uptime"] = (datetime.now() - self.start_time).total_seconds()
        
        # Get individual agent statuses
        if self.flow:
            status["triage_status"] = "active" if self.current_task == "triage" else "idle"
            status["context_status"] = "active" if self.current_task == "context" else "idle"
            status["strategist_status"] = "active" if self.current_task == "strategy" else "idle"
            status["composer_status"] = "active" if self.current_task == "compose" else "idle"
        
        return status
    
    async def train_agents(self, training_config: Dict[str, Any]):
        """Train agents with custom data"""
        try:
            await broadcast_agent_event("training_started", training_config)
            
            if training_config.get("use_historical"):
                # Load historical data from database
                training_data = await self._load_historical_data(training_config["user"])
            else:
                training_data = training_config.get("custom_data", [])
            
            if training_config["type"] == "fine_tune":
                # Implement fine-tuning logic
                await self._fine_tune_models(training_data)
            elif training_config["type"] == "few_shot":
                # Implement few-shot learning
                await self._update_few_shot_examples(training_data)
            
            await broadcast_agent_event("training_completed", {
                "type": training_config["type"],
                "samples": len(training_data)
            })
            
        except Exception as e:
            print(f"Training error: {e}")
            await broadcast_agent_event("training_failed", {"error": str(e)})
    
    async def update_model_preferences(self, preferences: Dict[str, str]):
        """Update model preferences for agents"""
        # Store preferences
        os.environ["AGENT_MODEL_PREFERENCES"] = json.dumps(preferences)
        
        # Update flow if running
        if self.flow:
            # Update crew models dynamically
            pass
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics"""
        db = SessionLocal()
        try:
            # Calculate metrics from logs
            logs = db.query(AgentLog).filter(
                AgentLog.created_at >= datetime.now() - timedelta(days=7)
            ).all()
            
            total_tokens = sum(log.total_tokens or 0 for log in logs)
            total_cost = sum(log.cost_usd or 0 for log in logs)
            successful = sum(1 for log in logs if log.success)
            failed = sum(1 for log in logs if not log.success)
            
            # Calculate response times
            response_times = [log.latency_ms for log in logs if log.latency_ms]
            avg_response = sum(response_times) / len(response_times) if response_times else 0
            
            # Model usage
            model_usage = {}
            for log in logs:
                if log.model_used:
                    model_usage[log.model_used] = model_usage.get(log.model_used, 0) + 1
            
            return {
                "avg_response_time": avg_response,
                "p95_response_time": self._calculate_percentile(response_times, 95),
                "p99_response_time": self._calculate_percentile(response_times, 99),
                "total_tokens": total_tokens,
                "estimated_cost": total_cost,
                "cost_per_email": total_cost / len(logs) if logs else 0,
                "success_rate": successful / (successful + failed) if (successful + failed) > 0 else 0,
                "error_rate": failed / (successful + failed) if (successful + failed) > 0 else 0,
                "model_usage": model_usage,
                "emails_per_hour": len(logs) / 168 if logs else 0  # Weekly average
            }
            
        finally:
            db.close()
    
    async def process_single_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single email through the pipeline"""
        from ..agents.crews.email_filter_crew import EmailFilterCrew
        
        crew = EmailFilterCrew()
        result = crew.process_emails([email])
        
        if result.get("success"):
            tasks = result.get("tasks", {})
            return {
                "category": self._extract_category(tasks.get("triage")),
                "priority": self._extract_priority(tasks.get("triage")),
                "context": tasks.get("context"),
                "strategy": tasks.get("strategy"),
                "draft": tasks.get("drafts")
            }
        
        return {"error": "Processing failed"}
    
    async def get_recent_logs(self, limit: int = 100) -> List[Dict]:
        """Get recent processing logs"""
        db = SessionLocal()
        try:
            logs = db.query(AgentLog).order_by(
                AgentLog.created_at.desc()
            ).limit(limit).all()
            
            return [log.to_dict() for log in logs]
            
        finally:
            db.close()
    
    async def _load_historical_data(self, user_email: str) -> List[Dict]:
        """Load historical email data for training"""
        from ..models.email import Email
        from ..models.draft import Draft
        
        db = SessionLocal()
        try:
            # Get successfully processed emails with drafts
            emails = db.query(Email, Draft).join(
                Draft, Email.gmail_id == Draft.email_id
            ).filter(
                Draft.status == "sent",
                Draft.user_email == user_email
            ).limit(100).all()
            
            training_data = []
            for email, draft in emails:
                training_data.append({
                    "input": {
                        "sender": email.sender_email,
                        "subject": email.subject,
                        "body": email.body,
                        "category": email.category.value if email.category else None
                    },
                    "output": {
                        "draft_subject": draft.subject,
                        "draft_body": draft.body
                    }
                })
            
            return training_data
            
        finally:
            db.close()
    
    async def _fine_tune_models(self, training_data: List[Dict]):
        """Fine-tune models with training data"""
        # Implement OpenAI fine-tuning
        pass
    
    async def _update_few_shot_examples(self, training_data: List[Dict]):
        """Update few-shot examples for agents"""
        # Store examples for use in prompts
        pass
    
    async def _log_error(self, error_type: str, error_message: str):
        """Log error to database"""
        db = SessionLocal()
        try:
            log = AgentLog(
                agent_name="system",
                action=error_type,
                success=False,
                error_message=error_message,
                created_at=datetime.now()
            )
            db.add(log)
            db.commit()
        finally:
            db.close()
    
    def _calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        if not values:
            return 0
        
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def _extract_category(self, triage_result: Any) -> str:
        """Extract category from triage result"""
        if isinstance(triage_result, str):
            try:
                data = json.loads(triage_result)
                if isinstance(data, list) and data:
                    return data[0].get("category", "uncategorized")
            except:
                pass
        return "uncategorized"
    
    def _extract_priority(self, triage_result: Any) -> int:
        """Extract priority from triage result"""
        if isinstance(triage_result, str):
            try:
                data = json.loads(triage_result)
                if isinstance(data, list) and data:
                    return data[0].get("priority", 3)
            except:
                pass
        return 3