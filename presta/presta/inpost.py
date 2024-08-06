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

def create_post_request(order_id: str, template: str) -> json:
    mpk = 0
    order = get_order(order_id)
    customer = get_cusomer(order['id_customer'])
    courier = get_courier(order['inpost_point'])
    address = get_address(order['id_address_delivery'])

    return json.dumps({
        "reference": "Zamówienie "+order_id,
        "mpk": mpk,
        "comments": order['note'],
        "receiver": create_receiver_form(courier, 
            company_name=address['company_name'],
            first_name=address['first_name'],
            last_name=address['last_name'],
            phone=address['phone'],
            email=customer['email'],
            address=create_address_form(
                street=address['street'],
                city=address['city'],
                post_code=address['post_code']
            ),
            ),
        "sender": sender,
        "parcels": create_parcels_form(template=template),
        "insurance": insurance,
        "cod": cod,
        "additional_services": create_custom_attributes(),
        "only_choice_of_offer": only_choice_of_offer,
        "is_return": is_return,
        "comments": order["note"]
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
