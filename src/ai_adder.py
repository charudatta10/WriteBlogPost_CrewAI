import os
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_loaders import AsyncChromiumLoader
import requests
from bs4 import BeautifulSoup
import logging
from crewai_tools import BaseTool, tool


# Initialize the Ollama model
ollama_model = Ollama(model="qwen:0.5b")


@tool
def multiplication_tool(url:str) -> str:
    """Useful for when you need to multiply two numbers together."""
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the desired data
        # Example: Extract all the headings
        headings = soup.find_all('href')
        for heading in headings:
            print(heading.text)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return first_number * second_number


# Define your agents with roles and goals
researcher = Agent(
    role='Teacher',
    goal='Teach addition',
    backstory="Give two numbers to the tool check output to be sum of nubers",
    verbose=True,
    allow_delegation=True,
    llm=ollama_model,
    tools=[multiplication_tool]  # Add tools to the writer agent
)

writer = Agent(
    role='Writer',
    goal='Create engaging content',
    backstory="You're a famous technical writer, specialized in writing data-related content",
    verbose=True,
    allow_delegation=True,  # Allow delegation to tools
    llm=ollama_model,
    tools=[multiplication_tool]  # Add tools to the writer agent
)

reviewer = Agent(
    role='Reviewer',
    goal='Review and grade articles',
    backstory="You're an experienced reviewer with a keen eye for detail",
    verbose=True,
    allow_delegation=False,
    llm=ollama_model
)

# Create tasks for your agents
task1 = Task(
    description='Teach addition provide two numbers to tool',
    expected_output="output of tool must be sum of two numbers",
    agent=researcher,
    tools=[multiplication_tool]
)

task2 = Task(
    description='Write a blog post on AI advancements',
    expected_output="Write an article blog post",
    agent=writer,
    #tools=["web_scraper", "pdf_indexer"],  # Delegate tasks to tools
    context=[task1]  # Set the context from the previous task
)

task3 = Task(
    description='Review and grade the blog post',
    expected_output="Provide a review and grade for the article",
    agent=reviewer,
    context=[task2]  # Set the context from the previous task
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[task1, task2, task3],
    llm=ollama_model,
    verbose=2,
    process=Process.sequential
)

# Error handling and logging
logging.basicConfig(level=logging.ERROR)

try:
    # Get your crew to work!
    result = crew.kickoff()
    
    print("Tasks completed successfully:", result)
except Exception as e:
    logging.error("An error occurred:", exc_info=True)

