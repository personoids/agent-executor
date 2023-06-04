import json
from langchain.llms.openai import OpenAI
from langchain.agents.agent_toolkits.openapi import planner
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.requests import RequestsWrapper
import requests
llm = OpenAI(model_name="gpt-4", temperature=0.0)

headers = {
}
requests_wrapper=RequestsWrapper(headers=headers)
response = requests.get('http://localhost:5004/openapi.json')
api_data = response.content

raw_personoids_api_spec = json.loads(api_data)
personoids_api_spec = reduce_openapi_spec(raw_personoids_api_spec)

personoids_agent = planner.create_openapi_agent(personoids_api_spec, requests_wrapper, llm)
user_query = "read what we have in the filesystem"
personoids_agent.run(user_query)