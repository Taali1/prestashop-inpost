import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import pandas as pd
import json

# Loading environmental variables
load_dotenv()
INPOST_API = os.getenv('INPOST_API')
base_url = 'https://api-shipx-pl.easypack24.net/'

def post_inpost(api_key: str) -> json:
    url = base_url + '/v1/organizations/73164/shipments'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    shipment = {

    }

    requests.post(url, headers=headers)




def get_inpost(api_key: str):
    url = base_url + 'v1/organizations/73164/shipments'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Shipments retrieved successfully")
        shipments = response.json()
        print(json.dumps(shipments, indent=4))
    else:
        print("Failed to retrieve shipments")
        print(response.status_code)
        print(response.text)


get_inpost(INPOST_API)

