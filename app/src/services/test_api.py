import requests
import os

from src.util.oauth import get_pecos_access_token
from src.util.local import load_local_env_vars

load_local_env_vars()
pecos_api_url = os.getenv('PECOS_URL_ROOT', None)
# url = pecos_api_url + 'model/providers'
url = 'https://val.cpiapi.cms.gov/api/1.0/ppr/providers'
# url = "https://cpianypointval.cms.gov/mocking/api/v1/sources/exchange/assets/51ece9dd-6045-4d01-b7c4-fe6856fdbdc0/exp" \
#       "-pecos-providers/1.0.35/m/providers"

def test_pecos_call():
    token = get_pecos_access_token()
    print(token)
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    body = {
        'providerID': {
            'providerType': 'ind',
            'npi': '5588776631'
        }
    }
    response = requests.post(url, headers=headers, data=body)
    return response.json()