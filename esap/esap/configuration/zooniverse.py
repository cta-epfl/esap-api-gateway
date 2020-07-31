
# title = "Zooniverse"
logo = "https://github.com/zooniverse/Brand/raw/master/style%20guide/logos/zooniverse-word/zooniverse-word-black.jpg"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename="esap-zooniverse"

# definition of the navigation bar
nav1 = {'title': 'Archives', 'route': '/archives'}
nav2 = {'title': 'Query', 'route': '/query'}
navbar = [nav1,nav2]

# if datasets_enabled is set, then only these datasets are visible to the GUI
#datasets_enabled = ['apertif-observations','astron.ivoa.obscore']

# if datasets_disabled is set, then all datasets except these are returned to the GUI
# datasets_disabled = ['nancay.ivoa.obscore']


# definition of the query
query_schema = {
  "name": "zooniverse",
  "title": "Zooniverse Projects Query",
  "type": "object",
  "properties": {
      "catalog": {
        "type": "string",
        "title": "Catalog",
        "default": "zooniverse_projects",
        "enum": ["all","zooniverse_projects", "zooniverse_workflows"],
        "enumNames": ["All","Projects", "Workflows"]
      },
    "panoptes_user": {
      "type": "string",
      "title": "Panoptes Username"
    },
    "panoptes_password": {
      "type": "string",
      "title": "Panoptes Password"
    },
  }
}

ui_schema = {
    "panoptes_password" : {
        "ui:widget" : "password"
    }
}
