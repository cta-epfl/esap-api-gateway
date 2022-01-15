
title = "CONCORDIA"
logo = "https://doublehi5.com/CONCORDIA-logo.png"

# definition of the query
query_schema = {
    "name": "concordia",
    "title": "CONCORDIA Query",
    "type": "object",
    "properties": {
        "workflow": {
            "type": "string",
            "title": "Workflow",
            "enum": ["Hello World"],
            "enumNames": ["Hello World"]
        },
        "inputs": {
            "type": "string",
            "title": "Optional Inputs",
        },
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "enum": ["concordia"],
            "enumNames": ["CONCORDIA"]
        },
        "jobid": {
            "type": "string",
            "title": "Job ID",
        }
    },
    "required": ["workflow"]
}

ui_schema = {"catalog": {"ui:widget": "hidden"}}


