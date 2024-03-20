from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
from langchain_core.tools import ToolException
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.messages import AIMessage, HumanMessage
import requests
import json
import concurrent.futures
# Local imports
from miksi_ai_sdk.sqltool import execute_query, get_database_schema
from miksi_ai_sdk.pythontool import *
from miksi_ai_sdk.api import MiksiAPIHandler

#db_info = get_database_schema()

def create_agent(miksi_api_key,media_path,instructions=None):
    
    # Custom input validation models for the execute_sql_query tool
    class SQLQueryInput(BaseModel):
        sql_query: str = Field(description="SQL query string to be executed")

    # Custom input validation models for the python interpreter tool
    class PythonCodeInput(BaseModel):
        code: str = Field(description="Python code to be executed")


    get_database_schema_tool = StructuredTool.from_function(
        func=get_database_schema,
        name="GetDatabaseSchema",
        description="Used to get database schema. Use this tool when you want to know how the database and its tables are like.",
    )


    execute_sql_query_tool = StructuredTool.from_function(
        func=execute_query,
        name="ExecuteSQLQuery",
        description="Takes in a correct SQL query and executes it to give results.",
        args_schema=SQLQueryInput,
    )

    execute_python_code_tool = StructuredTool.from_function(
        func=execute_code,
        name="ExecutePythonCode",
        description="Takes in  correct python code and executes it to give results.",
        args_schema=PythonCodeInput,
    )


    tools = [get_database_schema_tool, execute_sql_query_tool,execute_python_code_tool]

    # Load the language model
    llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=1.0)

    # Define prompt template with memory placeholders
    MEMORY_KEY = "chat_history"
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", f"""You are a very powerful and honest assistant with specific tools.You have get_database_schema_tool that 
            helps you see the db schema,execute_sql_query_tool that will execute correct sql code provided to it
            to give results,execute_python_code_tool that you can use to generate graphs/charts/tables by providing 
            correct python code to it.If an SQL query returns data store it in data structures like arrays and list 
            and pass the variable name do not directly pass the raw data to avoid violating context limit
            To use the pythoncode tool just provide the correct code that will be ecexuted
            to it.Dont directly provide raw data to it but use data structures like arrays and list to store results
            then use them to execute python code. Strictly use the tools dont do your own things
            ALWAYS return the SQL query that you executed and your reasoning 
            you used to answer the question as part of your final. Sometimes when the questions are not direct
            you need to make decisions on how to utilize these tools to provide the best answer to the questions asked
            answer.Dont suggest to the user the actions they should take instead take these actions yourself
            and just provide the answer to the question. For the questions that require your creativity be as 
            creative but STRICTLY explain your reasoning and what you did. When using matplotlib dont show the
            graph instead save it in {media_path} - matplotlib code should
             create this directory if doesnt exist-  in the current base directory. When you generate
            a graph label it well, and metion you generate a graph and return the path to saved graph in your final
            response.

            The only allowed file types you can generate are images(so if you generate a table e.g it has to be in image
            format). The following modules are already installed and you can utilise them for questions that require
            your creativity: # The agents default modules are :["matplotlib", "scikit-learn", "numpy", "statsmodels", "pandas",
              "scipy"]. The questions asking for trends/forecasting will need you to reason highly, deal with 
              errors such as incorrect date formatting since you are an intelligent agent.
              Try and explain the graphs from what you observe from the plotting data
            "IF THE QUESTION IS VAGUE JUST LOOK AT THE DATA,DECIDE YOURSELF AND COME UP WITH AN ANSWER!
            Strictly Give your final response in json format with the followings keys 1. answer- which is your
            final anwer from your observation, sql_queries.
            which is a list all the sql queries you executed to get to the answer, python-code which is python codes you 
            executed to get to the answer, and image_url which is the path to graph(s)/chart(s) you may have 
            generated.Strictly adhere to that format for all responses. 
            Below is the template for all your responses
            
            
            answer: 
                "Your final answer from your observations here.
            ,
            sql_queries:  "all SQL queries executed here
            ,
            python-code: python code that may have been used to plot graphs/charts/tables or other activity otherwise leave this blank,
            "image_url": 
                image paths here for all images generated, otherwise if no image generated also leave it blank
            
            Dont format your answer as a string it should be standard JSON, so dont enclose it in  ```json  ```

            If you ecounter a module not found error just run pip install <module_name> in the python tool
            If you dont find the answer or if an error occurs just simply give the answer as an error occurred
            try again dont given irrevant answer in respect to the question. 
            Below are the instructions you MUST follow! The below instructions can overide the ones provided above :
             {instructions}
            It is very important you follow all those instructions. I insist, It is very important you follow all those instructions"""),

            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Bind the tools to the language model
    llm_with_tools = llm.bind_tools(tools)

    try:
        api_handler = MiksiAPIHandler(miksi_api_key=miksi_api_key)
        response = api_handler.validate_miksi_api_key()
        validation=response['status']
    except Exception as e:
        print(f"An error occured while attempting to valid your Miksi API key: {e}")
    if validation:
        try:
            # Create the agent
            agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
                    "chat_history": lambda x: x.get(MEMORY_KEY, []),
                }
                | prompt_template
                | llm_with_tools
                | OpenAIToolsAgentOutputParser()
            )

            # Initialize the AgentExecutor with the agent and tools
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)
            print("Agent is Ready!")
            return agent_executor
        except Exception as e:
            print(f"An error occurred while creating the agent: {e}")
            return None
    


def send_user_question_async(miksi_api_key, query):
    main_url = 'http://127.0.0.1:8000'
    data = {'user_api_key': miksi_api_key, 'human_query': query}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(f'{main_url}/miksi/user-questions/', data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return None

def run_agent(agent,miksi_api_key, query):
    chat_history = []
    input1 = query
    if agent is not None:
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(send_user_question_async, miksi_api_key, query)
                result1 = agent.invoke({"input": input1, "chat_history": chat_history})
                chat_history.extend([HumanMessage(content=input1), AIMessage(content=result1["output"])])
                print("answer: " ,result1["output"])
                response = future.result()  # Wait for the API call to complete
                if response:
                    print("User question sent successfully.")
                else:
                    print("Failed to send user question.")
        except Exception as e:
            print(f"An Error occurred when running the agent: {e}")
    else:
        print(f"Agent instance not Established")

