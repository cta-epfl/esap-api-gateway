import requests
import urllib.parse
import json

zenodo_url="https://zenodo.org/api"
ZENODO_AUTH_TOKEN="REMOVED"

title = "Zenodo"
logo = "https://blog.zenodo.org/static/img/logos/zenodo-gradient-1000.png"

# definition of the query
query_schema = {
    "name": "zenodo",
    "title": "Zenodo Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Communities",
            "title": "Catalog",
            "enum": ["zenodo"],
            "enumNames": ["Zenodo"]
        }
    }
}

ui_schema = {"catalog": {"ui:widget": "hidden"}}
