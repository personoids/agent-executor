# flake8: noqa

from langchain.prompts.prompt import PromptTemplate


API_PLANNER_PROMPT = """You are a planner that plans the next API call to assist with user queries against an API.

You should:
1) evaluate which is the best method from the  API documentated below to solve the user query. 
2) generate the API call

You should only use API endpoints documented below ("Endpoints you can use:").
The plan will be passed to an API controller that can format it into web requests and return the responses.

----

Here are some examples:

User query: research how to use GCP through an npm package
Plan: POST /webSearch with query to find information about Google Cloud Platform SDK.

----

Here are endpoints you can use. Do not reference any of the endpoints above.

{endpoints}

----

User query: {query}
Plan:"""
API_PLANNER_TOOL_NAME = "api_planner"
API_PLANNER_TOOL_DESCRIPTION = f"Can be used to generate the next API call to assist with a user query, like {API_PLANNER_TOOL_NAME}(query). Should always be called before trying to call the API controller."

# Execution.
API_CONTROLLER_PROMPT = """You are an agent that gets an API call and given its documentation, execute it and return the final response.



Here is documentation on the API:
Base url: {api_url}
Endpoints:
{api_docs}


Here are tools to execute requests against the API: {tool_descriptions}


Starting below, you should follow this format:

Plan: the plan of API calls to execute
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the output of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I am finished executing the plan (or, I cannot finish executing the plan without knowing some other information.)
Final Answer: the final output from executing the plan or missing information I'd need to re-plan correctly.


Begin!

Plan: {input}
Thought:
{agent_scratchpad}
"""
API_CONTROLLER_TOOL_NAME = "api_controller"
API_CONTROLLER_TOOL_DESCRIPTION = f"Can be used to execute a plan of API calls, like {API_CONTROLLER_TOOL_NAME}(plan)."

# Orchestrate planning + execution.
# The goal is to have an agent at the top-level (e.g. so it can recover from errors and re-plan) while
# keeping planning (and specifically the planning prompt) simple.
API_ORCHESTRATOR_PROMPT = """You are an agent that assists with user queries against API, things like querying information or creating resources.
all user queries can be resolved in a single API call. you need to find the most appropriate parameters from the OpenAPI spec
You should always plan your API calls first, and then execute the plan second.
You should never return information without executing the api_controller tool.
Whenever bootstrap is mentioned in the user query, you should first call the /bootstrapPlugin endpoint

Here are the tools to plan and execute API requests: {tool_descriptions}


Use the format below for all of the responses, including failures
Starting below, you should follow this format:

User query: the query a User wants help with related to the API
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I am finished executing a plan and have the information the user asked for or the data the user asked to create
Final Answer: the final output from executing the plan


Example:
User query: can you find me some trendy stuff
Thought: I should plan an API call first.
Action: api_planner
Action Input: I need to find the right API call to find trendy items
Observation: GET /items with params 'trending' is 'True' to get trending item ids
Thought: I'm ready to execute the API calls.
Action: api_controller
Action Input: GET /items params 'trending' is 'True' to get trending item ids
...


Begin!

User query: {input}
Thought: I should generate a plan to help with this query and then copy that plan exactly to the controller.
{agent_scratchpad}"""

REQUESTS_GET_TOOL_DESCRIPTION = """Use this to GET content from a website.
Input to the tool should be a json string with 3 keys: "url", "params" and "output_instructions".
The value of "url" should be a string. 
The value of "params" should be a dict of the needed and available parameters from the OpenAPI spec related to the endpoint. 
If parameters are not needed, or not available, leave it empty.
The value of "output_instructions" should be instructions on what information to extract from the response, 
for example the id(s) for a resource(s) that the GET request fetches.
"""

PARSING_GET_PROMPT = PromptTemplate(
    template="""Here is an API response:\n\n{response}\n\n====
Your task is to extract some information according to these instructions: {instructions}
When working with API objects, you should usually use ids over names.
If the response indicates an error, you should instead output a summary of the error.

Output:""",
    input_variables=["response", "instructions"],
)

REQUESTS_POST_TOOL_DESCRIPTION = """Use this when you want to POST to a website.
Input to the tool should be a json string with 3 keys: "url", "data", and "output_instructions".
The value of "url" should be a string.
The value of "data" should be a dictionary of key-value pairs you want to POST to the url.
The value of "output_instructions" should be instructions on what information to extract from the response, for example the id(s) for a resource(s) that the POST request creates.
Always use double quotes for strings in the json string."""

PARSING_POST_PROMPT = PromptTemplate(
    template="""Here is an API response:\n\n{response}\n\n====
Your task is to extract some information according to these instructions: {instructions}
When working with API objects, you should usually use ids over names. Do not return any ids or names that are not in the response.
If the response indicates an error, you should instead output a summary of the error.

Output:""",
    input_variables=["response", "instructions"],
)

REQUESTS_PATCH_TOOL_DESCRIPTION = """Use this when you want to PATCH content on a website.
Input to the tool should be a json string with 3 keys: "url", "data", and "output_instructions".
The value of "url" should be a string.
The value of "data" should be a dictionary of key-value pairs of the body params available in the OpenAPI spec you want to PATCH the content with at the url.
The value of "output_instructions" should be instructions on what information to extract from the response, for example the id(s) for a resource(s) that the PATCH request creates.
Always use double quotes for strings in the json string."""

PARSING_PATCH_PROMPT = PromptTemplate(
    template="""Here is an API response:\n\n{response}\n\n====
Your task is to extract some information according to these instructions: {instructions}
When working with API objects, you should usually use ids over names. Do not return any ids or names that are not in the response.
If the response indicates an error, you should instead output a summary of the error.

Output:""",
    input_variables=["response", "instructions"],
)

REQUESTS_DELETE_TOOL_DESCRIPTION = """ONLY USE THIS TOOL WHEN THE USER HAS SPECIFICALLY REQUESTED TO DELETE CONTENT FROM A WEBSITE.
Input to the tool should be a json string with 2 keys: "url", and "output_instructions".
The value of "url" should be a string.
The value of "output_instructions" should be instructions on what information to extract from the response, for example the id(s) for a resource(s) that the DELETE request creates.
Always use double quotes for strings in the json string.
ONLY USE THIS TOOL IF THE USER HAS SPECIFICALLY REQUESTED TO DELETE SOMETHING."""

PARSING_DELETE_PROMPT = PromptTemplate(
    template="""Here is an API response:\n\n{response}\n\n====
Your task is to extract some information according to these instructions: {instructions}
When working with API objects, you should usually use ids over names. Do not return any ids or names that are not in the response.
If the response indicates an error, you should instead output a summary of the error.

Output:""",
    input_variables=["response", "instructions"],
)
