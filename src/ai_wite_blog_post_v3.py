import os
import logging
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool
from langchain_community.llms import Ollama

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AIProject:
    def __init__(self, model_name: str, research_topic: str, research_area: str):
        self.ollama_model = Ollama(model=model_name)
        self.research_topic = research_topic
        self.research_area = research_area
        self.researcher = self.create_researcher()
        self.writer = self.create_writer()
        self.crew = self.create_crew()

    def create_researcher(self) -> Agent:
        return Agent(
            role='Researcher',
            goal=f'Discover new insights in {self.research_area}',
            backstory="You're a world-class researcher working at a major data science company",
            verbose=True,
            allow_delegation=False,
            llm=self.ollama_model,
            tools=[ScrapeWebsiteTool()]
        )

    def create_writer(self) -> Agent:
        return Agent(
            role='Writer',
            goal='Create engaging content',
            backstory="You're a famous technical writer, specialized in writing data-related content",
            verbose=True,
            allow_delegation=False,
            llm=self.ollama_model
        )

    def create_tasks(self) -> list:
        task1 = Task(
            description=f'Investigate the latest trends in {self.research_topic} using web scraping',
            expected_output=f"Create a bullet report on the latest trends in {self.research_topic}",
            agent=self.researcher
        )

        task2 = Task(
            description=f'Write a blog post on advancements in {self.research_topic}',
            expected_output="Write an article blog post",
            agent=self.writer
        )

        return [task1, task2]

    def create_crew(self) -> Crew:
        tasks = self.create_tasks()
        return Crew(
            agents=[self.researcher, self.writer],
            tasks=tasks,
            llm=self.ollama_model,
            verbose=2,
            process=Process.sequential
        )

    def kickoff(self):
        try:
            logging.info("Starting the crew kickoff process.")
            result = self.crew.kickoff()
            logging.info("Crew kickoff process completed successfully.")
            print(result)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    research_topic = input("Enter the research topic: ")
    research_area = input("Enter the research area: ")
    project = AIProject(model_name="qwen:0.5b", research_topic=research_topic, research_area=research_area)
    project.kickoff()
