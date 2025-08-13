# backend/agents/crews/email_filter_crew.py
"""
Email Filter Crew - Main CrewAI implementation for email processing
"""

import os
import json
from typing import List, Dict, Any
from datetime import datetime

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from ..tools.gmail_tool import GmailTool
from ..tools.search_tool import SearchTool
from ..tools.draft_tool import DraftTool

# Load environment variables
load_dotenv()


@CrewBase
class EmailFilterCrew:
    """Email processing crew with specialized agents"""
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    def __init__(self):
        """Initialize the crew with LLM configurations"""
        # Initialize LLMs with different models for different agents
        self.llm_openai_mini = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.llm_openai = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.llm_gemini = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Initialize tools
        self.gmail_tool = GmailTool()
        self.search_tool = SearchTool()
        self.draft_tool = DraftTool()
        self.serper_tool = SerperDevTool()
    
    @agent
    def email_triage_specialist(self) -> Agent:
        """Agent for email classification and prioritization"""
        return Agent(
            config=self.agents_config["email_triage_specialist"],
            tools=[self.serper_tool],
            llm=self.llm_openai_mini,
            verbose=True,
            allow_delegation=False,
            max_retry_limit=2,
            memory=True,
            system_template="""You are an expert email classifier. 
            Always preserve original email metadata.
            Provide confidence scores for all classifications."""
        )
    
    @agent
    def context_analyzer(self) -> Agent:
        """Agent for deep context and thread analysis"""
        return Agent(
            config=self.agents_config["context_analyzer"],
            tools=[self.gmail_tool, self.search_tool],
            llm=self.llm_gemini,  # Gemini for long context
            verbose=True,
            allow_delegation=True,
            max_retry_limit=3,
            memory=True,
            system_template="""You excel at understanding email context.
            Analyze thread history and extract actionable insights.
            Consider sender relationships and communication patterns."""
        )
    
    @agent
    def response_strategist(self) -> Agent:
        """Agent for response strategy planning"""
        return Agent(
            config=self.agents_config["response_strategist"],
            tools=[self.search_tool],
            llm=self.llm_openai,
            verbose=True,
            allow_delegation=False,
            max_retry_limit=2,
            memory=True,
            system_template="""You are a strategic communication expert.
            Create response strategies that achieve desired outcomes.
            Consider tone, timing, and professional etiquette."""
        )
    
    @agent
    def draft_composer(self) -> Agent:
        """Agent for composing email drafts"""
        return Agent(
            config=self.agents_config["draft_composer"],
            tools=[self.draft_tool],
            llm=self.llm_openai,
            verbose=True,
            allow_delegation=False,
            max_retry_limit=2,
            memory=True,
            system_template="""You are a professional email writer.
            Compose clear, effective responses matching the required tone.
            Use [PLACEHOLDER] tags for missing information."""
        )
    
    @task
    def triage_emails(self) -> Task:
        """Task for email classification"""
        return Task(
            config=self.tasks_config["triage_emails"],
            agent=self.email_triage_specialist()
        )
    
    @task
    def analyze_context(self) -> Task:
        """Task for context analysis"""
        return Task(
            config=self.tasks_config["analyze_context"],
            agent=self.context_analyzer()
        )
    
    @task
    def plan_responses(self) -> Task:
        """Task for response planning"""
        return Task(
            config=self.tasks_config["plan_responses"],
            agent=self.response_strategist()
        )
    
    @task
    def compose_drafts(self) -> Task:
        """Task for draft composition"""
        return Task(
            config=self.tasks_config["compose_drafts"],
            agent=self.draft_composer()
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Email Filter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            cache=True,
            max_rpm=10,
            share_crew=False,
            output_log_file="logs/crew_output.log",
            task_callback=self._task_callback,
            step_callback=self._step_callback
        )
    
    def _task_callback(self, task_output):
        """Callback for task completion"""
        print(f"✅ Task completed: {task_output.task}")
        print(f"📊 Output: {task_output.raw[:200]}...")
        
    def _step_callback(self, step_output):
        """Callback for each step"""
        print(f"🔄 Step: {step_output}")
    
    def process_emails(self, emails: List[Dict[str, Any]], user_context: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Process a batch of emails through the crew
        
        Args:
            emails: List of email dictionaries
            user_context: User information for personalization
            
        Returns:
            Processing results with drafts
        """
        if user_context is None:
            user_context = {
                "user_name": os.getenv("USER_NAME", "User"),
                "user_company": os.getenv("USER_COMPANY", "Company"),
                "user_role": os.getenv("USER_ROLE", "Professional")
            }
        
        inputs = {
            "emails_json": json.dumps(emails),
            **user_context
        }
        
        try:
            print(f"🚀 Processing {len(emails)} emails...")
            result = self.crew().kickoff(inputs=inputs)
            
            # Parse and structure the results
            processed_result = self._parse_results(result)
            
            # Save results
            self._save_results(processed_result)
            
            return processed_result
            
        except Exception as e:
            print(f"❌ Error processing emails: {str(e)}")
            raise
    
    def _parse_results(self, result) -> Dict[str, Any]:
        """Parse crew results into structured format"""
        try:
            return {
                "success": True,
                "processed_at": datetime.now().isoformat(),
                "raw_output": result.raw,
                "tasks": {
                    "triage": result.tasks_output.get("triage_emails"),
                    "context": result.tasks_output.get("analyze_context"),
                    "strategy": result.tasks_output.get("plan_responses"),
                    "drafts": result.tasks_output.get("compose_drafts")
                },
                "token_usage": result.token_usage,
                "status": "completed"
            }
        except Exception as e:
            print(f"⚠️ Error parsing results: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "raw_output": str(result),
                "status": "error"
            }
    
    def _save_results(self, results: Dict[str, Any]):
        """Save processing results to files"""
        os.makedirs("output", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/email_processing_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to {filename}")