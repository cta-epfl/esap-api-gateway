#import requests
#import urllib.parse
#import json

title = "CONCORDIA"
logo = "https://doublehi5.com/CONCORDIA-logo.png"

# definition of the query
query_schema = {
    "name": "concordia",
    "title": "CONCORDIA Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "enum": ["concordia"],
            "enumNames": ["CONCORDIA"]
        }
    }
}
ui_schema = {"catalog": {"ui:widget": "hidden"}}

