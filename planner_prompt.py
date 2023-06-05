# flake8: noqa

from langchain.prompts.prompt import PromptTemplate


API_PLANNER_PROMPT = """You are a planner that plans the next API call to assist with user queries against an API.

You should:
1) evaluate which is the best method from the API documentated below to solve the user query. use only methods from the api endpoints documented below. fallback to /shellExecute if you can't find a better endpoint to use.
2) generate a single API call to one of the endpoints description including the context.

You should only use API endpoints documented below ("Here are endpoints you can use...").
The plan will be passed to an API controller that can format it into a web request and return the response.

----

Here are some examples:

User query: research how to use GCP through an npm package
Plan: POST /webSearch - 'query' to find information about Google Cloud Platform SDK. include bootstrap_auth_token in the request body.

User query: install GCP SDK for nodejs
Plan: POST /shellExecute - 'command' to install GCP SDK for nodejs. include bootstrap_auth_token in the request body.

User query: bootstrap
Plan: POST /bootstrapPlugin

----

Here are endpoints you can use:

{endpoints}


notice that almost all of them are POST requests!
----

User query: {query}
Plan:"""
API_PLANNER_TOOL_NAME = "api_planner"
API_PLANNER_TOOL_DESCRIPTION = f"Can be used to generate the next API call to assist with a user query, like {API_PLANNER_TOOL_NAME}(query). Should always be called before trying to call the API controller."

# Execution.
API_CONTROLLER_PROMPT = """You are an agent that gets an API call and given its documentation, execute it and return the final response.

you can run shell/linux/bash commands using an POST request to /shellExecute


Here is documentation on the API:
Base url: {api_url}
Endpoints:
{api_docs}
"""
API_CONTROLLER_TOOL_NAME = "api_controller"
API_CONTROLLER_TOOL_DESCRIPTION = f"Can be used to execute an API call, like {API_CONTROLLER_TOOL_NAME}(plan)."

# Orchestrate planning + execution.
# The goal is to have an agent at the top-level (e.g. so it can recover from errors and re-plan) while
# keeping planning (and specifically the planning prompt) simple.
API_ORCHESTRATOR_PROMPT = f"""You are an agent that can fulfill any user query against the plugin using API calls, things like querying information, creating resources, coding, running shell commands, etc.
all user queries can be resolved in a single API call. you need to find the most appropriate parameters from the OpenAPI spec.
You should always plan your API call first, and then execute the plan second.
You should never return information without executing the api_controller tool.
if you get an invalid token error. you should POST to the /bootstrapPlugin endpoint and return all the result. especially the auth_token, then pass it to every subsequent call as bootstrap_auth_token.
you can run shell/linux/bash commands using an POST request to /shellExecute.
you should always return the entire response from the API call or from the tool you used.
"""

REQUESTS_GET_TOOL_DESCRIPTION = """Use this when you want to perform a GET request
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

REQUESTS_POST_TOOL_DESCRIPTION = """Use this when you want to perform a POST request
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
