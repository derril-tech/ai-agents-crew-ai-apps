from pathlib import Path
import yaml

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from content_marketing_project_manager.types import ProjectPlan


@CrewBase
class ContentMarketingProjectManager:
    """Content Marketing Project Manager Crew"""

    def __init__(self) -> None:
        # Resolve config paths relative to this file (works with src/ layout)
        base_path = Path(__file__).parent / "config"
        agents_file = base_path / "agents.yaml"
        tasks_file = base_path / "tasks.yaml"

        # Load YAML into dictionaries
        with agents_file.open("r", encoding="utf-8") as f:
            self.agents_config = yaml.safe_load(f)
        with tasks_file.open("r", encoding="utf-8") as f:
            self.tasks_config = yaml.safe_load(f)

    # --- Agents ---
    @agent
    def project_planning_agent(self) -> Agent:
        return Agent(config=self.agents_config["project_planning_agent"], verbose=False)

    @agent
    def estimation_agent(self) -> Agent:
        return Agent(config=self.agents_config["estimation_agent"], verbose=False)

    @agent
    def resource_allocation_agent(self) -> Agent:
        return Agent(config=self.agents_config["resource_allocation_agent"], verbose=False)

    # --- Tasks ---
    @task
    def task_breakdown(self) -> Task:
        return Task(
            config=self.tasks_config["task_breakdown"],
            agent=self.project_planning_agent(),
        )

    @task
    def time_resource_estimation(self) -> Task:
        return Task(
            config=self.tasks_config["time_resource_estimation"],
            agent=self.estimation_agent(),
        )

    @task
    def resource_allocation(self) -> Task:
        return Task(
            config=self.tasks_config["resource_allocation"],
            agent=self.resource_allocation_agent(),
            output_pydantic=ProjectPlan,
        )

    # --- Crew ---
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.project_planning_agent(),
                self.estimation_agent(),
                self.resource_allocation_agent(),
            ],
            tasks=[
                self.task_breakdown(),
                self.time_resource_estimation(),
                self.resource_allocation(),
            ],
            process=Process.sequential,  # Planner -> Estimator -> Allocator
            verbose=False,
        )
