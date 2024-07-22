import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import pandas as pd
import json

# Loading environmental variables
load_dotenv()
PRESTA_API = os.getenv('PRESTA_API')
base_url = 'https://pracownia-firan.pl/sklep/api'

def get_orders_request(api_key: str):
    url = f"{base_url}/orders"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(api_key, ''))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_order_request(api_key: str, order_id):
    url = f"{base_url}/orders/{order_id}"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(api_key, ''))

    if response.status_code == 200:
        return response.json()['order']

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_orders(api_key: str):
    result = []
    id_list = get_orders_request(api_key)['orders']
    columns = ['id', 'id_address_delivery', 'id_cart', 'id_address_invoice', 'id_customer', 'current_state', 'valid', 'date_add', 'note', 'total_paid_real', 'associations']

    for order_id in id_list:
        result += [get_order_request(api_key, order_id['id'])]
        print(f'{order_id["id"]}: Pass')

    df = pd.DataFrame(result)
    return df[columns]

def write_orders_csv(df_orders):
    print('df written orders data')
    df_orders.to_csv('orders_data.txt', sep='\t', index=False)

def get_clients(api_key: str, customer_id):
    url = f"{base_url}/customers/{customer_id}"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(api_key, ''))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_address(api_key: str, address_id):
    url = f"{base_url}/address/{address_id}"
    headers = {'Output-Format': 'JSON'}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(api_key, ''))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def create_sender_form(company_name: str, email: str, phone: str, address: json) -> json:
    try:
        if address:
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


def create_parcels_form( height: float, length: float, width: float, weight_amount: float, id: str = "package") -> json:
    try:    
        # in InPost default unit is mm
        # height, length, width [float]
        dimensions = {
            "height": height,
            "length": length,
            "width": width
        }

        # in InPost default unit is kg
        # weight_amount [float]
        weight = {
            "weight_amount": weight_amount
        }

        if dimensions and weight:
            return json.dumps([{
                "id": id, # idk losowe id = package
                "dimensions": dimensions,
                "wieght": weight
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

def create_receiver_form(company_name: str, first_name: str, last_name: str, phone: str, email: str, address: str) -> json:
# company_name [str(255)] - wymagany gdy nie jest podany adres, imie, nazwisko
# first_name [str] - wymagany gdy nie jest podany email, phone, company_name
# last_name [str] - wymagany gdy nie jest podany email, phone, company_name
# phone [str(9)] - zawsze wymagane
# email [str] - wymagany w momencie przesyłki paczkomatem
# address [form] - wymagany gdy wysyłana kurierem
    try:
        if company_name: # wysyłka do firmy
            if address: # kurier
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
            if address: # kurier
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



print(get_orders(PRESTA_API))
