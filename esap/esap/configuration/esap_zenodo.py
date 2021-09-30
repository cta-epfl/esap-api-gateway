#import requests
#import urllib.parse
#import json

title = "Zenodo"
logo = "https://blog.zenodo.org/static/img/logos/zenodo-gradient-1000.png"

# definition of the query
query_schema = {
    "name": "zenodo",
    "title": "Zenodo Query",
    "type": "object",
    "properties": {
        #"community": {
            #"type": "string",
            #"title": "community",
        #},
        "keyword": {
            "type": "string",
            "title": "keyword",
        },
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "enum": ["zenodo"],
            "enumNames": ["Zenodo"]
        }
    },
    #"required": ["community"]
}
ui_schema = {"keyword": {"ui:help": "e.g. CTA", "ui:placeholder": "optional"}, "catalog": {"ui:widget": "hidden"}}
#ui_schema = {"keyword": {"ui:help": "e.g. CTA"}, 
#      "community": {"ui:help": "*required", "ui:placeholder": "escape2020"},"catalog": {"ui:widget": "hidden"}}

