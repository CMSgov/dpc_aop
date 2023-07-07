import os
import requests
from src.util.local import load_local_env_vars

# The string returned from this function should be passed into the Authorization
# header for any requests to the PECOS API, with the following format:
# Authorization: Bearer {token}
def get_pecos_access_token() -> str:
    load_local_env_vars()
    url = os.getenv('PECOS_API_TOKEN_URL', None)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'cache-control': 'no-cache'
    }
    params = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('PECOS_CLIENT_ID', None),
        'client_secret': os.getenv('PECOS_CLIENT_SECRET', None),
        'scope': 'READ'
    }
    response = requests.post(url, headers=headers, params=params)
    json = response.json()
    return json['access_token']
