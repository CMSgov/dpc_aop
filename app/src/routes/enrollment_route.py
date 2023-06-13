import flask
import requests


url = "https://cpianypointval.cms.gov/mocking/api/v1/sources/exchange/assets/51ece9dd-6045-4d01-b7c4-fe6856fdbdc0/exp" \
      "-pecos-providers/1.0.35/m/providers"


def get_ao_information(npi: str) -> flask.Response:
    # get provider ID from NPI
    payload = {
        "providerID": {
            "npi": npi,
        }
    }
    provider_response = requests.post(url, data=payload)
    provider = provider_response.json["provider"]
    payload["identity"] = {
        "idType": provider["idType"],
        "id": provider["id"],
    }

    # get current enrollment ID from provider ID and NPI
    enrollment_response = requests.post(url + "/enrollments", data=payload)
    enrollment_id = enrollment_response.json["enrollments"]

    # get AO from current enrollment roles
    role_response = requests.get(url + "/enrollments/" + enrollment_id + "/roles")
    roles = role_response.json["enrollments"]["roles"]
    ao_role = next(iter(role for role in roles if role["roleCode"] == "10"), None)
    if not ao_role:
        raise
    return ao_role["names"]
