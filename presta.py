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
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_orders(api_key: str):
    result = []
    id_list = get_orders_request(api_key)['orders']

    for order_id in id_list:
        result += [get_order_request(api_key, order_id['id'])]
        print(f'{order_id["id"]}: Pass')

    df = pd.DataFrame(result)
    columns = ['id', 'id_address_delivery', 'id_cart', 'id_address_invoice', 'id_customer', 'current_state', 'valid', 'date_add', 'note', 'total_paid_real', 'associations']
    df = df[columns]

    return df 


df = get_orders(PRESTA_API)
print('df written')

df.to_csv('orders_data.txt', sep='\t', index=False)
