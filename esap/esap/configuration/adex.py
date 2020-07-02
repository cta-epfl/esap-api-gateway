
# title = "ADEX"
logo = "https://alta.astron.nl/alta-static/images/esap/adex_logo.png"

# title = "ESFRI Science Analysis Platform"
#logo = "http://uilennest.net/static/media/tree9.da598501.png"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename="esap-gui"

# definition of the navigation bar
nav1 = {'title': 'Archives', 'route': '/archives'}
nav2 = {'title': 'Query', 'route': '/query'}
navbar = [nav1,nav2]

# if datasets_enabled is set, then only these datasets are visible to the GUI
#datasets_enabled = ['apertif-observations','astron.ivoa.obscore']

# if datasets_disabled is set, then all datasets except these are returned to the GUI
datasets_disabled = ['nancay.ivoa.obscore']


# definition of the query
query_schema = {
  "name": "adex",
  "title": "ASTRON Data Collection Query",
  "type": "object",
  "properties": {
    "catalog": {
      "type": "string",
      "title": "Catalog",
      "default": "apertif",
      "enum": ["all","apertif", "astron_vo"],
      "enumNames": ["All","Apertif", "ASTRON_VO"]
    },
    "target": {
      "type": "string",
      "title": "Target"
    },
    "ra": {
      "type": "number",
      "title": "RA (degrees)",
    },
    "dec": {
      "type": "number",
      "title": "dec (degrees)",
    },
    "fov": {
      "type": "number",
      "title": "search radius (degrees)",
    },
    "level": {
      "type": "string",
      "title": "DataProduct Level",
      "default": "raw",
      "enum": ["all","raw","processed"],
      "enumNames": ["All","Raw","Processed"]
    },
    "category": {
      "type": "string",
      "title": "Keywords",
    },
  }
}