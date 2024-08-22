import requests
import os
from dotenv import load_dotenv
import json
from presta_import import *


# Loading environmental variables
load_dotenv()
INPOST_API = os.getenv('INPOST_API')
base_url = 'https://api-shipx-pl.easypack24.net/'

def post_inpost(api_key: str, data) -> json:
    url = base_url + 'v1/organizations/73164/shipments'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    return response

def create_post_request(order_id: str, template: str) -> json:
    order = get_order(order_id)
    customer = get_customer(order['id_customer'])
    courier = get_courier(order['inpost_point'])
    address = get_address(order['id_address_delivery'])
    print(address)
    return json.dumps({
        "reference": "Zamówienie "+str(order_id),
        "comments": order['note'],
        "receiver": create_receiver_form(courier=courier, 
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
        "parcels": create_parcels_form(template=template, id=order_id),
        "insurance": "inpost_courier_standard",
#        "additional_services": create_custom_attributes(),
        "only_choice_of_offer": True,
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

post_request = create_post_request(49, "A")

print(json.dumps(post_request, indent=4, ensure_ascii=False))

response = post_inpost(INPOST_API, post_request)

try:
    response_json = response.json()
    # Wyprintowanie sformatowanego JSON-a
    print(json.dumps(response_json, indent=4, ensure_ascii=False))
except ValueError:
    # Jeśli odpowiedź nie jest JSON-em, wyprintuj tekst
    print(response.text)