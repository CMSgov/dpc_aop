import os
import requests

def get_pecos_access_token() -> dict[str, str]:
    url = os.getenv('PECOS_API_TOKEN_URL', None)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'cache-control': 'no-cache'
    }
    params = {
        'grant_type': os.getenv('PECOS_GRANT_TYPE', None),
        'client_id': os.gentenv('PECOS_CLIENT_ID', None),
        'client_secret': os.getnev('PECOS_CLIENT_SECRET', None),
        'scope': os.getenv('PECOS_CLIENT_SCOPE', None)
    }
    response = requests.post(url, headers=headers, params=params)
    return response.json()
