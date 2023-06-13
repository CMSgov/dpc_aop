import flask
import requests


url = "https://cpianypointval.cms.gov/mocking/api/v1/sources/exchange/assets/51ece9dd-6045-4d01-b7c4-fe6856fdbdc0" \
      "/exp-pecos-providers/1.0.35/m/providers"


def get_from_response(items: List[Dict[str]], key: str, value: str):
    # extract the element from a list of dicts for which a given key matches a value.
    # assumes match is found for no more than one element.
    return next(iter(item for item in items if item[key] == value), None)


def get_ao_information(npi: str, include_fala: bool = False, include_sanctions: bool = False) -> flask.Response:
    # get provider ID from NPI, along with FALA and med sanctions if requested
    payload = {
        "providerID": {
            "npi": npi,
        }
    }
    headers = {
        "dataSets": {
            "fala": include_fala,
            "medSanctions": include_sanctions,
        }
    }
    provider_response = requests.post(url, data=payload, headers=headers)
    provider = provider_response.json["provider"]
    fala = provider.get("fala", None)
    med_sanctions = provider.get("medSanctions", None)
    payload["identity"] = {
        "idType": provider["idType"],
        "id": provider["id"],
    }

    # get current enrollment ID from provider ID and NPI
    enrollment_response = requests.post(url + "/enrollments", data=payload)
    enrollments = enrollment_response.json["enrollments"]
    active_enrollment = get_from_response(enrollments, "status", "ACTIVE")
    if not active_enrollment:
        raise
    enrollment_id = active_enrollment["enrollmentID"]

    # get AO from current enrollment roles
    role_response = requests.get(url + "/enrollments/" + enrollment_id + "/roles")
    roles = role_response.json["enrollments"]["roles"]
    ao_role = get_from_response(roles, "roleCode", "10")
    if not ao_role:
        raise
    return {
        "names": ao_role["names"],
        "fala": fala,
        "medSanctions": med_sanctions,
    }
