Miksi AI agent works with a couple of tools to give you the final value. Mostly its an interchange between a tool that executes SQL query and the one that executes the python code to generate graphs 

While the agent is instructed to strictly not to execute code that writes/ modifies the data, We advice you provide a database user with only read permission to the agent

The python code to generate graphs/charts/tables is executed withing a separate virtual environment. This environment is created by default during agent initialization, at the base directory -you will see a directory called  venvs . All the agents dependencies in relation to python will be installed here - for instance matplotlip for graphics and charts. So this will be totally independent of any other virtual environments you are running

The generated graphs/charts by default are saved in a directory called media at the base directory - By base directory we mean relative to where you are running the scripts that utilizes our agent.

# Connecting to the databse 
Miksi Abstracts conecting to your SQL database into a sequence of two simple steps, provide credentials, and call the connection function

from miksi_ai_sdk.sqltool import set_database_config,check_db_config_variables
set_database_config will set the database credentials while check_db_config_variables() will report back if any of those credentials hasnt been set or is none

# Connecting to the database
set_database_config(db_name,db_user,db_password,db_host,db_port)

Keep this open when running the agent since the connection closes after every operation

print(f"db credentials{check_db_config_variables()}")

We now start setting up the agent by initializing python environement

# Initialize python environment
from miksi_ai_sdk.master import initialize_env

initialize_env(env_path)

The above method will intialize an existing environment or create a new one in case none exists in the specified path. Some default standard python  modules will also be installed so this process may take some minutes when configuring/setting up for the first time

env_path as an argument is the location you wish to create this virtual environment

# Additional installs 
Miksi AI gives you the flexibility to run additional installations for python and instruct the agent to use them. For instance you can install matplotlib and ask the agent to use it for generating graphs/charts,  or you can prefer another standard module such as plotly or seaborn. This is entirely upon you. By default matplotlin is the default plotting library. This is also a great way to debug import not found error. 

To install additional modules, run 

from miksi_ai_sdk.master import safe_install_modules

safe_install_modules(['modules_here'])


# Creating the agent
Miksi AI agent is context aware, accepts custom instructions in natural language (e.g give the answer in Slovakian), and helps maintain the states. It accepts user questions and uses the tools inside virtual environments to arrive to the final answer
Provide your own instructions in natural language(e.g a sample on how to format the final answer or the language to give the final answer in)

from miksi_ai_sdk.agent import create_agent

# Creating the agent
instructions = ''
agent = create_agent(media_path= media_path, instructions=instructions)

media path is the directory where you wanted generated graphs/images/charts to be saved for rendering in your application


# Running the agent
query = "your query here"
answer = run_agent(agent, query)
