# This file is part of [Your Project Name]
#
# Copyright (C) 2024 Charudatta
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os 
from crewai import Agent, Task, Crew, Process  
from langchain_community.llms import Ollama 

ollama_model = Ollama(model="gemma:2b")   

 
# # Define your agents with roles and goals 
researcher = Agent(   role='Researcher',
                      goal='Discover new insights',
                      backstory="You're a world class researcher working on a major data science company",
                      verbose=True,
                      allow_delegation=False,  
                      llm=ollama_model
                      ) 

writer = Agent(   role='Writer',
                  goal='Create engaging content',   
                  backstory="You're a famous technical writer, specialized on writing data related content",   
                  verbose=True,
                  allow_delegation=False,
                  llm=ollama_model
                  )  

# Create tasks for your agents 
task1 = Task(description='Investigate the latest AI trends', 
             expected_output="Create bullet report on latest ai trends", 
             agent=researcher
             ) 

task2 = Task(description='Write a blog post on AI advancements', 
             expected_output="write a article blog post", 
             agent=writer)  

# Instantiate your crew with a sequential process - TWO AGENTS! 
crew = Crew(   agents=[researcher, writer],
               tasks=[task1, task2],   
               llm=ollama_model,    
               verbose=2,    
               process=Process.sequential  
               )  

# Get your crew to work! 
result = crew.kickoff()
