import json
from langchain.llms.openai import OpenAI
import planner 
from spec import reduce_openapi_spec

from langchain.requests import RequestsWrapper
import requests

personoids_agent = planner.create_openapi_agent(
    reduce_openapi_spec(json.loads(requests.get('http://localhost:5004/openapi.json').content)), 
    requests_wrapper=RequestsWrapper(), 
    llm=OpenAI(model_name="gpt-4", temperature=0.0)
    )
user_query = "boostrap and learn gcp"
personoids_agent.run(user_query)