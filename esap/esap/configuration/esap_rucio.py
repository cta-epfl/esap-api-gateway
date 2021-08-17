import requests
import urllib.parse
import json
from django.conf import settings

ID_TOKEN_KEY = "oidc_id_token"
ACCESS_TOKEN_KEY = "oidc_access_token"

def validate(token):
    url = urllib.parse.urljoin(f"{settings.RUCIO_HOST}", "rses/")
    response = requests.get(
        url, headers={"X-Rucio-Auth-Token": token}, verify=False
    )
    if response.ok:
        return True
    else:
        # remove
        return False


def get_scope_names(session):
    token = session.get(ACCESS_TOKEN_KEY, None)
    # id_token = session.get(ID_TOKEN_KEY, None)

    if token is None:
       return [f"Not logged in {session}, {session.keys()}."]

    validated = validate(token)
    if validated:
        url = urllib.parse.urljoin(f"{settings.RUCIO_HOST}", "scopes")
        response = requests.get(
            url + "/", headers={"X-Rucio-Auth-Token": token}, verify=False
        )
        if response.ok:
            return json.loads(response.content)
        else:
            return [
                "validated but failed query"
            ]  # , val_response.status_code, val_response.reason]
    else:
        return [f"not validated, {len(token)}, {type(token)}, '{token}'."]  # , val_response.status_code, val_response.reason]
    # except Exception as e:
    #     return ["Failed", "Authentication", e]


class Config:
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

    ui_schema = {"catalog": {"ui:widget": "hidden"}}

    def __init__(self, session):
        self.session=session
        self.__query_schema = self.gen_query_schema()

    @property
    def query_schema(self):
        return self.__query_schema

    def gen_query_schema(self):
        scope_names = get_scope_names(self.session)
        return {
            "name": "rucio",
            "title": "Rucio Query",
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "title": "Scope",
                    "enum": scope_names,
                    "enumNames": scope_names,
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
