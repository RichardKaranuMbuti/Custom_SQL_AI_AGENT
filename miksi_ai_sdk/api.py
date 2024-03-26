import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
base_url = "https://miksiapi-miksi.pythonanywhere.com/"

api_url = "https://miksiapi-miksi.pythonanywhere.com/miksi/validate_api/"

default_model_url= "https://miksiapi-miksi.pythonanywhere.com/miksi/get_default_model/"

class MiksiAPIHandler:
    def __init__(self,miksi_api_key):
        self.api_url = api_url
        self.miksi_api_key = miksi_api_key
        self.main_url="https://miksiapi-miksi.pythonanywhere.com"

    def __str__(self):
        return "MiksiAPIHandler Instance"

    def validate_miksi_api_key(self):
        miksi_api_key_url = "https://miksiapi-miksi.pythonanywhere.com/miksi/validate_miksi_api_key/"
        
        try:
            # Prepare the data for the POST request
            data = {
                'miksi_api_key': self.miksi_api_key
            }

            # Make the POST request with a timeout
            response = requests.post(miksi_api_key_url, data=data, timeout=10)
            print("response:", response)

            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                print("response_Data", response_data)
                return response_data
            else:
                logger.error(f"Failed to call API. Status Code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None


    def get_openai_data(self):
        validation_result = self.validate_miksi_api_key()
        validation=validation_result['status']
        if validation:
            try:
                openai_response = requests.get(f'{self.main_url}/miksi/openais/') 
                openai_response.raise_for_status()
                openai_data = openai_response.json()  
                if openai_data:
                    return openai_data[0]
                else:
                        return None                    
            except Exception as e:
                logging.error(f"Error in get_openai_data: {e}")
                return None
        else:
            return None
        
    def get_azure_openai_data(self):
        validation_result = self.validate_miksi_api_key()
        validation=validation_result['status']
        if validation:
            try:
                azureopenai_response = requests.get(f'{self.main_url}/miksi/azure-openais/')
                azureopenai_response.raise_for_status()
                azureopenai_data = azureopenai_response.json()
                if azureopenai_data:
                    return azureopenai_data[0]
                else:
                    return None
            
            except Exception as e:
                logging.error(f"Error in get_openai_data: {e}")
                return None
        else:
            return None


'''
# Example usage of the class
import os
miksi_api_key = os.getenv('miksi_api_key')
api_handler = MiksiAPIHandler(miksi_api_key=miksi_api_key)
status = api_handler.validate_miksi_api_key()
data =api_handler.get_openai_data()
print(f"openai data: {data}")
print("API status", status)
'''