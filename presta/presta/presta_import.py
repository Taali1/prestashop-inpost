import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import pandas as pd
import json

# Loading environmental variables
load_dotenv()
PRESTA_API = os.getenv('PRESTA_API')
BASE_URL = 'https://pracownia-firan.pl/sklep/api'

def get_orders_request():
    url = f"{BASE_URL}/orders"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(PRESTA_API, ''))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_courier(inpost_point: str) -> json:
    if inpost_point:
        return False
    else:
        return True

def get_order(order_id):
    url = f"{BASE_URL}/orders/{order_id}"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(PRESTA_API, ''))

    if response.status_code == 200:
        return response.json()['order']

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_address(address_delivery_id: str):
    url = f"{BASE_URL}/addresses/{address_delivery_id}"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(PRESTA_API, ''))

    if response.status_code == 200:
        address = response.json()['address']
        return {
            "company_name": address["company"],
            'first_name': address['firstname'],
            'last_name': address['lastname'],
            "street": address['address1'] + ' ' + address['address2'],
            'post_code': address['postcode'],
            'city': address['city'],
            'phone': address['phone']
            }
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_orders():
    result = []
    id_list = get_orders_request()['orders']

    for order_id in id_list:
        result += [get_order(order_id['id'])]
        print(f'{order_id["id"]}: Pass')

    return result

def get_cusomer(customer_id):
    url = f"{BASE_URL}/customers/{customer_id}"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(PRESTA_API, ''))

    if response.status_code == 200:
        return response.json()['customer']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def create_sender_form(company_name: str, email: str, phone: str, address: json, courier: bool) -> json:
    try:
        if courier:
            return json.dumps({
                "company_name": company_name,
                "email": email,
                "phone": phone,
                "address": address
            })
        else:
            return json.dumps({
                "company_name": company_name,
                "email": email,
                "phone": phone
            })
    except Exception as error:
        print(error)

def create_cod_form(amount: int, currency: str = 'PLN') -> json:
    # in InPost default currency is PLN
    try:
        return json.dumps({
            "amount": amount,
            "currency": currency
        })
    except Exception as error:
        print(error)


def create_insurance(amount: int, currency: str = "PLN") -> json:
    # in InPost default currency is PLN
    try:
        return json.dumps({
            "amount": amount,
            "currency": currency
        })
    except Exception as error:
        print(error)


def create_parcels_form(template: str, id: str = "package") -> json:
    try:    
        if template:
            return json.dumps([{
                "id": id+template, # idk losowe id = package
                "template": template
            }])
    except Exception as error:
        print(error)

# wymagane w przypadku paczkomatu
def create_custom_attributes(target_point: str) -> json:
    try:
        return json.dumps({
            "target_point": target_point
        })
    except Exception as error:
        print(error)


def create_address_form(street: str, city: str, post_code: str) -> json:
# street [str(255)] - wymagane
# city [str(255)] - wymagane
# post_code [str(6)] - wymagane (np. 00-000)
    try:
        return json.dumps({
            "street": street,
            "city": city,
            "post_code": post_code
        })
    except Exception as error:
        print(error)

def create_receiver_form(
    company_name: str, 
    first_name: str, 
    last_name: str, 
    phone: str, 
    email: str, 
    address: str, 
    courier: bool) -> json:
# company_name [str(255)] - wymagany gdy nie jest podany adres, imie, nazwisko
# first_name [str] - wymagany gdy nie jest podany email, phone, company_name
# last_name [str] - wymagany gdy nie jest podany email, phone, company_name
# phone [str(9)] - zawsze wymagane
# email [str] - wymagany w momencie przesyłki paczkomatem
# address [form] - wymagany gdy wysyłana kurierem
    try:
        if company_name: # wysyłka do firmy
            if courier: # kurier
                return json.dumps({
                    "company_name": company_name,
                    "phone": phone,
                    "email": email,
                    "address": address
                })
            else: # paczkomat
                return json.dumps({
                    "company_name": company_name,
                    "phone": phone,
                    "email": email
                })
        
        if first_name and last_name: # wysyłka do osoby prywatnej
            if courier: # kurier
                return json.dumps({
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "email": email,
                    "address": address
                })
            else: # paczkomat
                return json.dumps({
                    "first_name": first_name,
                    "last_name": last_name,    
                    "phone": phone,
                    "email": email
                })
    except Exception as error:
        print(error)


def get_test(id: str):
    url = f"{BASE_URL}/orders/{id}"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(PRESTA_API, ''))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


print(json.dumps(get_test(49)["order"]["note"], indent=4))
