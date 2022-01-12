
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
            "enum": ["CTA", "KM3NeT"],
            "enumNames": ["CTA", "KM3NeT"]
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
        },
        "username": {
            "type": "string",
            "title": "Username",
        }
    },
    "required": ["workflow"]
}

ui_schema = {"catalog": {"ui:widget": "hidden"}}


