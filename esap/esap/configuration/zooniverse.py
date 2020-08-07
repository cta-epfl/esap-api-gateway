from zooniverse_fields import project_fields, workflow_fields

# title = "Zooniverse"
logo = "https://github.com/zooniverse/Brand/raw/master/style%20guide/logos/zooniverse-word/zooniverse-word-black.jpg"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename = "esap-zooniverse"

# definition of the navigation bar
nav1 = {"title": "Archives", "route": "/archives"}
nav2 = {"title": "Query", "route": "/query"}
navbar = [nav1, nav2]

# if datasets_enabled is set, then only these datasets are visible to the GUI
# datasets_enabled = ['apertif-observations','astron.ivoa.obscore']

# if datasets_disabled is set, then all datasets except these are returned to the GUI
# datasets_disabled = ['nancay.ivoa.obscore']

pFields = project_fields()
wFields = workflow_fields()

# definition of the query
query_schema = {
    "name": "zooniverse",
    "title": "Zooniverse Projects Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "enum": ["zooniverse_projects", "zooniverse_workflows"],
            "enumNames": ["Projects", "Workflows"],
        },
        "panoptes_user": {"type": "string", "title": "Panoptes Username"},
        "panoptes_password": {"type": "string", "title": "Panoptes Password"},
    },
    "required": ["panoptes_user", "panoptes_password", "catalog"],
    "dependencies": {
        "catalog": {
            "oneOf": [
                {
                    "properties": {
                        "catalog": {"enum": ["zooniverse_projects"]},
                        "project_fields": {
                            "type": "array",
                            "title": "Extra Project Fields  (Default is all fields)",
                            "items": {
                                "type": "string",
                                "enum": pFields,
                                "enumNames": [
                                    field.replace("_", " ").title() for field in pFields
                                ],
                            },
                            "uniqueItems": True,
                        },
                    }
                },
                {
                    "properties": {
                        "catalog": {"enum": ["zooniverse_workflows"]},
                        "workflow_fields": {
                            "type": "array",
                            "title": "Extra Workflow Fields (Default is all fields)",
                            "items": {
                                "type": "string",
                                "enum": wFields,
                                "enumNames": [
                                    field.replace("_", " ").title() for field in wFields
                                ],
                            },
                            "uniqueItems": True,
                        },
                    }
                },
            ]
        }
    },
}

ui_schema = {"panoptes_password": {"ui:widget": "password"}}
