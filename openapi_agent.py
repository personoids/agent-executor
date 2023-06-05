import json
from langchain.llms.openai import OpenAI
import planner 
from spec import reduce_openapi_spec

from langchain.requests import RequestsWrapper
import requests

personoids_agent = planner.create_openapi_agent(
    reduce_openapi_spec(json.loads(requests.get('http://localhost:5004/openapi.json').content)), 
    requests_wrapper=RequestsWrapper(), 
    llm=OpenAI(model_name="gpt-4", temperature=0.9)
    )
personoids_agent.run("bootstrap")
personoids_agent.run("clone the most popular gitlab repository")
personoids_agent.run("auto-proceed")
personoids_agent.run("auto-proceed")
personoids_agent.run("auto-proceed")
personoids_agent.run("auto-proceed")
personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")



# sub_agent = Tool(func=personoids_agent, description="can do anything")
# agent 

