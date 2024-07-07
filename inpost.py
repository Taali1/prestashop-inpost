import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import pandas as pd

# Loading environmental variables
load_dotenv()
INPOST_API = os.getenv('INPOST_API')
base_url = 'https://pracownia-firan.pl/sklep/api'




def post_inpost(api_key: str):
    pass

def get_inpost(api_key: str):
    pass