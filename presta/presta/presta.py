import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import pandas as pd

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


write_orders_csv(get_orders(PRESTA_API))
