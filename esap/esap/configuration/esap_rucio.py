import requests
import urllib.parse
import json

rucio_url = "https://escape-rucio.cern.ch"

AUTH_PORT = 32301
STANDARD_PORT = 32300

RUCIO_AUTH_TOKEN = "<REDACTED>"


def validate():
    url = urllib.parse.urljoin(f"{rucio_url}:{AUTH_PORT}", "auth/validate")
    response = requests.get(
        url, headers={"X-Rucio-Auth-Token": RUCIO_AUTH_TOKEN}, verify=False
    )
    if response.ok:
        return True
    else:
        return False


def get_scope_names():
    # try:
    validated = validate()
    if validated:
        url = urllib.parse.urljoin(f"{rucio_url}:{STANDARD_PORT}", "scopes")
        response = requests.get(
            url + "/", headers={"X-Rucio-Auth-Token": RUCIO_AUTH_TOKEN}, verify=False
        )
        if response.ok:
            return json.loads(response.content)
        else:
            return [
                "validated but failed query"
            ]  # , val_response.status_code, val_response.reason]
    else:
        # , val_response.status_code, val_response.reason]
        return ["not validated"]
    # except Exception as e:
    #     return ["Failed", "Authentication", e]


title = "Rucio"
logo = "http://rucio.cern.ch/images/wide_logo2.png"

# definition of the query
query_schema = {
    "name": "rucio",
    "title": "Rucio Query",
    "type": "object",
    "properties": {
        "scope": {
            "type": "string",
            "title": "Scope",
            "enum": get_scope_names(),
            "enumNames": get_scope_names(),
        },
        "resource_category": {
            "type": "string",
            "title": "Category",
            "enum": ["files", "dids", "replicas"],
            "enumNames": ["Files", "DIDs", "Replicas"],
            "default": "dids",
        },
        "catalog": {
            "type": "string",
            "enum": ["esap_rucio_entities"],
            "enumNames": ["esap_rucio_entities"],
            "default": "esap_rucio_entities",
        },
    },
}

ui_schema = {"catalog": {"ui:widget": "hidden"}}
