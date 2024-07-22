import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import json
from presta_import import *


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

def create_post_request(
    mpk: str,                                       # skąd ma pobierać opłatę z przesyłkę
    receiver: json,                                 #
    sender: json,                                   #
    parcels: json,                                  # [form] - cechy paczki (wymiary, waga)
    cod: json,                                      # [form] - wartość z pobraniem 
    insurance: json,                                # [form] - ubezpieczenie
    reference: str,                                 # dodatkowy opis przesyłki, tutaj id zamówienia
    is_return: bool = False,                        # czy jest to zwort 
    comments: str = "",                             #
    only_choice_of_offer: bool = True,              # jeżeli True to tworzy przesyłkę bez opłaty, w inpost defaultowo jest False tzn. tworzenie i opłata
    additional_services: list = ['sms', 'email']    #
    ):

    return json.dumps({
        "reference": reference,
        "mpk": mpk,
        "comments": comments,
        "receiver": receiver,
        "sender": sender,
        "parcels": parcels,
        "insurance": insurance,
        "cod": cod,
        "additional_services": additional_services,
        "only_choice_of_offer": only_choice_of_offer,
        "is_return": is_return
    })



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

