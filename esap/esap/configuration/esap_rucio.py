import requests
import os
import json

rucio_url = "https://escape-rucio.cern.ch"

AUTH_PORT = 32301
STANDARD_PORT = 32300

RUCIO_AUTH_TOKEN = "grange-/DC=org/DC=terena/DC=tcs/C=NL/O=ASTRON/CN=Robot - Yan Grange 1086@astron.nl-unknown-809a62ca07bb471cac3012b6af752c86"

def validate():
    url = os.path.join(f"{rucio_url}:{AUTH_PORT}", "auth", "validate")
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
        url = os.path.join(f"{rucio_url}:{STANDARD_PORT}", "scopes")
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
        return ["not validated"]  # , val_response.status_code, val_response.reason]
    # except Exception as e:
    #     return ["Failed", "Authentication", e]


title = "Rucio"
logo = "http://rucio.cern.ch/images/wide_logo2.png"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename = "esap-rucio"

# definition of the navigation bar
nav1 = {"title": "Archives", "route": "/archives"}
nav2 = {"title": "Query", "route": "/query"}
navbar = [nav1, nav2]

# if datasets_enabled is set, then only these datasets are visible to the GUI
# datasets_enabled = ['apertif-observations','astron.ivoa.obscore']

# if datasets_disabled is set, then all datasets except these are returned to the GUI
# datasets_disabled = ['nancay.ivoa.obscore']

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
            "enum": ["files", "dids"],
            "enumNames": ["Files", "DIDs"],
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
