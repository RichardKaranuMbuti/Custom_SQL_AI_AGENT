import os
from panafrican_ai.api import MiksiAPIHandler
from dotenv import load_dotenv
load_dotenv()

miksi_api_key = os.getenv('miksi_api_key')
print(miksi_api_key)
api_handler = MiksiAPIHandler(miksi_api_key=miksi_api_key)
status = api_handler.validate_miksi_api_key()
data =api_handler.get_openai_data()
print(f"openai data: {data}")
print("API status", status)