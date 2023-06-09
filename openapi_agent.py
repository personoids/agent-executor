import json
from langchain.llms.openai import OpenAI
import planner 
from spec import reduce_openapi_spec

from langchain.requests import RequestsWrapper
import requests

bootstrap_data = json.loads(requests.post('http://localhost:5004/bootstrapPlugin').content)
boot = "bootstrap_auth_token=" + bootstrap_data["auth_token"] + "\n"
boot += bootstrap_data["assistantInstructions"] + "\n"
print(boot)
personoids_agent = planner.create_openapi_agent(
    reduce_openapi_spec(json.loads(requests.get('http://localhost:5004/openapi.json').content)), 
    requests_wrapper=RequestsWrapper(), 
    llm=OpenAI(model_name="gpt-4", temperature=0.9, max_tokens=3000, verbose=True),
    instructions=boot,
    instructions_planner=boot,
    instructions_controller=boot,
    )
# print(bootstrap_data["assistantInstructions"])
# print(bootstrap_data["proxyFrom"])
# print(bootstrap_data["nextInstructions"])

# personoids_agent.run(boot)

# personoids_agent.run("bootstrap and show the results")
# print("bootstrap and show the results")
print("clone the most popular gitlab repository")
result = personoids_agent.run("clone the most popular gitlab repository")
print(result)
# print("auto-proceed")
# personoids_agent.run("proceed until done")
def auto_proceed(): 
    print("auto-proceed ")
    personoids_agent.run(f"result: {result}. \n\n auto-proceed" )
attempts = 0
try:
    while attempts < 5:
        auto_proceed()
        attempts += 1
except Exception as e:
    print("Failed. " + str(e))
    while attempts < 5:
        auto_proceed()
        attempts += 1

# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")
# personoids_agent.run("auto-proceed")



# sub_agent = Tool(func=personoids_agent, description="can do anything")
# agent 

