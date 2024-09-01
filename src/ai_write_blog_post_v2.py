import os
import logging
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool
from langchain_community.llms import Ollama

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Ollama model
ollama_model = Ollama(model="qwen:0.5b")

# Define your agents with roles and goals
researcher = Agent(
    role='Researcher',
    goal='Discover new insights',
    backstory="You're a world-class researcher working at a major data science company",
    verbose=True,
    allow_delegation=False,
    llm=ollama_model,
    tools=[ScrapeWebsiteTool()]
)

writer = Agent(
    role='Writer',
    goal='Create engaging content',
    backstory="You're a famous technical writer, specialized in writing data-related content",
    verbose=True,
    allow_delegation=False,
    llm=ollama_model
)

# Create tasks for your agents
task1 = Task(
    description='Investigate the latest AI trends using web scraping',
    expected_output="Create a bullet report on the latest AI trends",
    agent=researcher
)

task2 = Task(
    description='Write a blog post on AI advancements',
    expected_output="Write an article blog post",
    agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    llm=ollama_model,
    verbose=2,
    process=Process.sequential
)

# Get your crew to work!
try:
    logging.info("Starting the crew kickoff process.")
    result = crew.kickoff()
    logging.info("Crew kickoff process completed successfully.")
    print(result)

except Exception as e:
    logging.error(f"An error occurred: {e}")
    print(f"An error occurred: {e}")
