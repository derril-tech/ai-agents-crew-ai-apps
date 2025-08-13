from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.sdr_assistant_flow.lead_types import GeneratedEmail
# from src.sdr_assistant_flow.tools.email_validator_tool import EmailValidatorTool

@CrewBase
class DraftColdEmailCrew:
    """Crew that crafts and optimizes personalized cold outreach emails based on lead profile and readiness."""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # === Agents ===
    @agent
    def cold_email_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['cold_email_copywriter'],
            tools=[],
            verbose=True,
            memory=True,
            max_iter=2
        )

    @agent
    def conversion_focus_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['conversion_focus_agent'],
            tools=[],
            verbose=True,
            memory=True,
            max_iter=2
        )

    # === Tasks ===
    @task
    def draft_personalized_cold_email(self) -> Task:
        return Task(
            config=self.tasks_config['draft_personalized_cold_email'],
            agent=self.cold_email_copywriter(),
            output_file='email_draft.md'
        )

    @task
    def optimize_for_response(self) -> Task:
        return Task(
            config=self.tasks_config['optimize_for_response'],
            agent=self.conversion_focus_agent(),
            context=[self.draft_personalized_cold_email()],
            output_pydantic=GeneratedEmail,
            output_file='final_email.json'
        )

    # === Crew Composition ===
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )