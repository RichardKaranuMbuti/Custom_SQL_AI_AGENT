from dotenv import load_dotenv
import openai
import os

from miksi_ai_sdk.sqltool import set_database_config,check_db_config_variables
from miksi_ai_sdk.master import initialize_env,install_defaults
from miksi_ai_sdk.master import safe_install_modules

from miksi_ai_sdk.agent import create_agent
from miksi_ai_sdk.agent import run_agent


load_dotenv()
miksi_api_key = os.getenv("miksi_api_key")

db_name = os.getenv('db_name')
print(db_name)
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host = os.getenv('db_host')
db_port = 5432

env_path = 'venvs'
media_path = 'media/images'

# Connecting to the database
set_database_config(db_name,db_user,db_password,db_host,db_port)

#print(f"db credentials{check_db_config_variables()}")

# Initialize python environment 
initialize_env(env_path)



#Additional installs
# The agents default modules are :["matplotlib", "scikit-learn", "numpy", "statsmodels", "pandas", "scipy"]
#safe_install_modules(['matplotlib']) if you want to install other modules


# checking connection status

from miksi_ai_sdk.utils import check_connection
from miksi_ai_sdk.utils import set_db

set_db(db_name,db_user,db_password,db_host,db_port)
status = check_connection(engine= 'PostgreSQL')

print(f"Connection status: {status}")

# Creating the agent
instructions = ''
engine = 'PostgreSQL'
agent = create_agent(miksi_api_key=miksi_api_key,media_path= media_path,
                     engine=engine, instructions=instructions)

from miksi_ai_sdk.utils import always_clean_json_formatter

# Running the agent
query = "how many students are in grade 9, also show a graph of students against grades"
answer = run_agent(agent,miksi_api_key, query)
print(f"answer: {answer}")



