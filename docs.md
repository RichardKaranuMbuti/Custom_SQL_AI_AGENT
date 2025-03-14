# Intro

Miksi AI agent works with a couple of tools to give you the final value. Mostly, it's an interchange between a tool that executes SQL queries and the one that executes the python code to generate graphs.

While the agent is instructed strictly not to execute code that writes/modifies the data, we advise you to provide a database user with only read permission to the agent.

The python code to generate graphs/charts/tables is executed within a separate virtual environment. This environment is created by default during agent initialization, at the base directory—you will see a directory called `venvs`. All the agent's dependencies in relation to python will be installed here—for instance, matplotlib for graphics and charts. So this will be totally independent of any other virtual environments you are running.

The generated graphs/charts by default are saved in a directory called `media` at the base directory. By base directory, we mean relative to where you are running the scripts that utilize our agent.

## **Install Miksi-AI SDK:**

- Install the latest version: `pip install miksi_ai_sdk`

The supported python versions are 
['3.7', '3.8', '3.9', '3.10', '3.11','3.12']


# Supported SQL based engines
The support SQL engines are MySQL, PostgreSQL, and MsSQL server


## Connecting to the Database

Miksi abstracts connecting to your SQL database into "you just provide credentials" and the rest is handled.

```python
from miksi_ai_sdk.sqltool import set_database_config, check_db_config_variables

 set_database_config will set the database credentials
# check_db_config_variables() will report back if any of those credentials hasn't been set or is None
set_database_config(db_name, db_user, db_password, db_host, db_port)
```

Keep this open when running the agent since the connection closes after every operation.

```python
print(f"db credentials: {check_db_config_variables()}")
```

# checking connection status
It's Important to first check if connection to your database is seamless. 
If you get a success connection status from the functions below then the agent will be able to connect to your engine seamlessly

Select and specify your engine from the list of supported engines belows
[MySQL, PostgreSQL, MsSQL] 

```python
from miksi_ai_sdk.utils import check_connection
from miksi_ai_sdk.utils import set_db

set_db(db_name,db_user,db_password,db_host,db_port)
status = check_connection(engine= 'MySQL')

print(f"Connection status: {status}")
```


We now start setting up the agent by initializing the python environment.

## Initialize Python Environment

```python
from miksi_ai_sdk.master import initialize_env

initialize_env(env_path)
```

The above method will initialize an existing environment or create a new one in case none exists in the specified path. Some default standard python modules will also be installed, so this process may take some minutes when configuring/setting up for the first time.

`env_path` as an argument is the location you wish to create this virtual environment.

## Additional Installs

Miksi AI gives you the flexibility to run additional installations for python and instruct the agent to use them. For instance, you can install matplotlib and ask the agent to use it for generating graphs/charts, or you can prefer another standard module such as plotly or seaborn. This is entirely upon you. By default, matplotlib is the default plotting library. This is also a great way to debug import not found error.

To install additional modules, run:

```python
from miksi_ai_sdk.master import safe_install_modules

safe_install_modules(['modules_here'])
```

## Creating the Agent

Miksi AI agent is context-aware, accepts custom instructions in natural language (e.g., give the answer in Slovakian), and helps maintain the states. It accepts user questions and uses the tools inside virtual environments to arrive at the final answer. Provide your own instructions in natural language (e.g., a sample on how to format the final answer or the language to give the final answer in).

```python
from miksi_ai_sdk.agent import create_agent

agent = create_agent(miksi_api_key=miksi_api_key, media_path=media_path, instructions=instructions)
```

**Get your API Key:**

- Visit [MiksiAPI](https://miksiapi-miksi.pythonanywhere.com), sign up or log in, then generate your API key. This API key will be used to use the Miksi SDK.

`media_path` is the directory where you wanted generated graphs/images/charts to be saved for rendering in your application.

## Running the Agent

```python
from miksi_ai_sdk.agent import run_agent

query = "your query here"
answer = run_agent(agent, query)
```



