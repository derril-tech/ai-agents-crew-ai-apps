"""
Updated CrewAI Sales Meeting Preparation with Fixed Tool Imports
This version handles tool import issues and provides fallback options
"""

import os
import yaml
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

# ================================
# TOOL IMPORTS WITH FALLBACKS
# ================================

# Try importing CrewAI tools with fallbacks
try:
    from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
    TOOLS_AVAILABLE = True
    print("✅ CrewAI tools imported successfully")
except ImportError as e:
    print(f"⚠️ CrewAI tools not available: {e}")
    print("💡 To install: pip install crewai-tools")
    TOOLS_AVAILABLE = False
    
    # Fallback: Create basic tool classes or use None
    class SerperDevTool:
        def __init__(self):
            print("⚠️ Using SerperDevTool fallback - web search may not work")
    
    class ScrapeWebsiteTool:
        def __init__(self):
            print("⚠️ Using ScrapeWebsiteTool fallback - web scraping may not work")
    
    class WebsiteSearchTool:
        def __init__(self):
            print("⚠️ Using WebsiteSearchTool fallback - website search may not work")

# Alternative: Use LangChain tools directly
try:
    from langchain_community.tools import DuckDuckGoSearchRun
    from langchain_community.document_loaders import WebBaseLoader
    LANGCHAIN_TOOLS_AVAILABLE = True
    print("✅ LangChain community tools available as backup")
except ImportError as e:
    LANGCHAIN_TOOLS_AVAILABLE = False
    print(f"⚠️ LangChain community tools not available: {e}")
    print("💡 To install: pip install langchain-community")

# ================================
# LLM SETUP
# ================================

# Initialize OpenAI LLM
try:
    openai_llm = ChatOpenAI(
        model="gpt-4o-mini",  # Using GPT-4o-mini for cost efficiency
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    print("✅ OpenAI LLM initialized successfully")
except Exception as e:
    print(f"❌ Error initializing OpenAI LLM: {e}")
    print("Please set OPENAI_API_KEY environment variable")
    exit(1)

# ================================
# CREW CLASS WITH TOOL FIXES
# ================================

@CrewBase
class SalesMeetingPreparation:
    """Sales Meeting Preparation Crew with Fixed Tool Imports"""
    
    # Use absolute paths to config files
    agents_config = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'agents.yaml')
    tasks_config = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'tasks.yaml')
    
    def __init__(self):
        print("🚀 Initializing Sales Meeting Preparation Crew...")
        
        # Load configuration files
        try:
            with open(self.agents_config, 'r', encoding='utf-8') as file:
                self.agents_config_data = yaml.safe_load(file)
            print("✅ Agents config loaded successfully")
        except FileNotFoundError:
            print(f"❌ agents.yaml not found at {self.agents_config}")
            print("Creating default config...")
            self.agents_config_data = self.create_default_agents_config()
        
        try:
            with open(self.tasks_config, 'r', encoding='utf-8') as file:
                self.tasks_config_data = yaml.safe_load(file)
            print("✅ Tasks config loaded successfully")
        except FileNotFoundError:
            print(f"❌ tasks.yaml not found at {self.tasks_config}")
            print("Creating default config...")
            self.tasks_config_data = self.create_default_tasks_config()
    
    def get_tools_for_agent(self, agent_type):
        """Return appropriate tools based on availability"""
        if TOOLS_AVAILABLE:
            if agent_type == "research":
                return [SerperDevTool(), ScrapeWebsiteTool()]
            elif agent_type == "profile":
                return [SerperDevTool(), WebsiteSearchTool()]
            elif agent_type == "strategist":
                return [SerperDevTool()]
        elif LANGCHAIN_TOOLS_AVAILABLE:
            # Use LangChain tools as fallback
            return [DuckDuckGoSearchRun()]
        else:
            # No tools available
            print("⚠️ No search tools available - agents will work with limited capabilities")
            return []
    
    @agent
    def company_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config_data['company_research_agent'],
            tools=self.get_tools_for_agent("research"),
            llm=openai_llm
        )
    
    @agent
    def executive_profile_agent(self) -> Agent:
        return Agent(
            config=self.agents_config_data['executive_profile_agent'],
            tools=self.get_tools_for_agent("profile"),
            llm=openai_llm
        )
    
    @agent
    def sales_pitch_strategist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config_data['sales_pitch_strategist_agent'],
            tools=self.get_tools_for_agent("strategist"),
            llm=openai_llm
        )
    
    @agent
    def report_quality_agent(self) -> Agent:
        return Agent(
            config=self.agents_config_data['report_quality_agent'],
            llm=openai_llm
        )
    
    def agents(self):
        """Return list of all agents"""
        return [
            self.company_research_agent(),
            self.executive_profile_agent(),
            self.sales_pitch_strategist_agent(),
            self.report_quality_agent()
        ]
    
    def tasks(self):
        """Return list of all tasks"""
        return [
            self.research_company_task(),
            self.profile_executive_task(),
            self.generate_sales_pitch_task(),
            self.finalize_report_task()
        ]
    
    @task
    def research_company_task(self) -> Task:
        return Task(
            config=self.tasks_config_data['research_company'],
            agent=self.company_research_agent()
        )
    
    @task
    def profile_executive_task(self) -> Task:
        return Task(
            config=self.tasks_config_data['profile_executive'],
            agent=self.executive_profile_agent()
        )
    
    @task
    def generate_sales_pitch_task(self) -> Task:
        return Task(
            config=self.tasks_config_data['generate_sales_pitch'],
            agent=self.sales_pitch_strategist_agent(),
            context=[
                self.research_company_task(),
                self.profile_executive_task()
            ]
        )
    
    @task
    def finalize_report_task(self) -> Task:
        return Task(
            config=self.tasks_config_data['finalize_report'],
            agent=self.report_quality_agent(),
            context=[
                self.research_company_task(),
                self.profile_executive_task(),
                self.generate_sales_pitch_task()
            ]
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Sales Meeting Preparation crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            llm=openai_llm  # Explicitly set the LLM
        )
    
    def create_default_agents_config(self):
        """Create default agents configuration if file doesn't exist"""
        config_dir = os.path.dirname(self.agents_config)
        os.makedirs(config_dir, exist_ok=True)
        
        default_config = {
            'company_research_agent': {
                'role': 'Company Research Specialist',
                'goal': 'Research and analyze company information thoroughly to prepare for sales meetings',
                'backstory': 'You are an expert company researcher with deep knowledge of business analysis, market research, and competitive intelligence. You excel at finding relevant information about companies, their business models, recent news, and market position.'
            },
            'executive_profile_agent': {
                'role': 'Executive Profiler',
                'goal': 'Create detailed profiles of executives to understand their background and interests',
                'backstory': 'You are a skilled executive researcher who specializes in profiling business leaders. You can find information about their career history, achievements, interests, and communication style to help tailor sales approaches.'
            },
            'sales_pitch_strategist_agent': {
                'role': 'Sales Strategy Specialist',
                'goal': 'Develop compelling sales pitches based on company and executive research',
                'backstory': 'You are an experienced sales strategist who excels at creating personalized and compelling sales pitches. You understand how to align product offerings with company needs and executive priorities.'
            },
            'report_quality_agent': {
                'role': 'Report Quality Analyst',
                'goal': 'Review and refine reports to ensure they are comprehensive and actionable',
                'backstory': 'You are a meticulous quality analyst who ensures all reports are well-structured, comprehensive, and provide actionable insights for sales teams.'
            }
        }
        
        with open(self.agents_config, 'w', encoding='utf-8') as file:
            yaml.dump(default_config, file, default_flow_style=False)
        
        return default_config
    
    def create_default_tasks_config(self):
        """Create default tasks configuration if file doesn't exist"""
        config_dir = os.path.dirname(self.tasks_config)
        os.makedirs(config_dir, exist_ok=True)
        
        default_config = {
            'research_company': {
                'description': 'Research the target company thoroughly including their business model, recent news, financial performance, market position, and key challenges. Focus on information that would be relevant for a sales meeting.',
                'expected_output': 'A comprehensive company research report including business overview, recent developments, market position, and potential pain points that our solution could address.'
            },
            'profile_executive': {
                'description': 'Create a detailed profile of the executive we will be meeting with, including their background, role, recent activities, interests, and communication style.',
                'expected_output': 'A detailed executive profile including background, current role, recent achievements, interests, and recommended approach for engagement.'
            },
            'generate_sales_pitch': {
                'description': 'Based on the company research and executive profile, create a compelling and personalized sales pitch that addresses the company\'s specific needs and resonates with the executive.',
                'expected_output': 'A tailored sales pitch presentation outline with key talking points, value propositions, and anticipated questions/objections.'
            },
            'finalize_report': {
                'description': 'Review all research and create a final comprehensive report that includes company analysis, executive profile, and sales strategy recommendations.',
                'expected_output': 'A polished, comprehensive sales meeting preparation report with executive summary, detailed findings, and actionable recommendations.'
            }
        }
        
        with open(self.tasks_config, 'w', encoding='utf-8') as file:
            yaml.dump(default_config, file, default_flow_style=False)
        
        return default_config

# ================================
# MAIN EXECUTION
# ================================

def main():
    """Main function to run the sales meeting preparation crew"""
    
    print("🎯 Starting Sales Meeting Preparation System")
    print("=" * 50)
    
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set. Please set your OpenAI API key:")
        print("\n🔧 Setup Instructions:")
        print("1. Get an OpenAI API key from: https://platform.openai.com/api-keys")
        print("2. Create a .env file in the backend directory:")
        print("   cp env.example .env")
        print("3. Edit .env and add your API key:")
        print("   OPENAI_API_KEY=your_actual_api_key_here")
        print("4. Or set it temporarily in PowerShell:")
        print("   $env:OPENAI_API_KEY = 'your-api-key-here'")
        print("\n💡 You can also use the test_setup.py script to verify your setup")
        return
    
    # Debug: Print environment variables
    print(f"🔍 Environment check:")
    print(f"   OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    print(f"   GROQ_API_KEY: {'Set' if os.getenv('GROQ_API_KEY') else 'Not set'}")
    print(f"   SERPER_API_KEY: {'Set' if os.getenv('SERPER_API_KEY') else 'Not set'}")
    
    try:
        # Initialize the crew
        sales_crew = SalesMeetingPreparation()
        crew = sales_crew.crew()
        
        # Example inputs - modify as needed
        inputs = {
            'company': 'OpenAI',
            'executive': 'Sam Altman',
            'meeting_date': '2024-12-15',
            'product_service': 'AI Development Platform'
        }
        
        print(f"🔍 Preparing for meeting with {inputs['executive']} at {inputs['company']}")
        print("⏳ This may take a few minutes...")
        
        # Run the crew
        result = crew.kickoff(inputs=inputs)
        
        print("✅ Sales meeting preparation completed!")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ Error running crew: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Ensure OPENAI_API_KEY is set correctly")
        print("2. Install missing dependencies:")
        print("   pip install -r requirements.txt")
        print("   pip install crewai-tools langchain-community")
        print("3. Check internet connection for API calls")
        print("4. Run test_setup.py to verify your setup")

if __name__ == "__main__":
    main()