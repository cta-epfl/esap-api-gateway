
#title = "ESAP"
#logo = "http://uilennest.net/static/media/tree9.da598501.png"

frontend_basename="esap-gui-dev"

logo = "https://alta.astron.nl/alta-static/images/esap/esap_logo.png"

# definition of the navigation bar
nav1 = {'title': 'Archives', 'route': '/archives'}
nav2 = {'title': 'Datasets', 'route': '/datasets'}
nav3 = {'title': 'Telescopes', 'route': '/telescopes'}
nav4 = {'title': 'Query', 'route': '/query'}
nav5 = {'title': 'Settings', 'route': '/about'}
navbar = [nav1,nav2,nav3,nav4,nav5]

# definition of the query
query_schema = {
  "title": "ESAP Query",
  "type": "object",
  "properties": {
    "institute": {
      "type": "string",
      "title": "Institute",
      "default": "all",
      "enum": ["all","Astron"],
      "enumNames": ["all","astron"]
    },

    "title": {
      "type": "string",
      "title": "Title",
      "default" : ""
    },
    "target": {
      "type": "string",
      "title": "Target"
    },
    "ra": {
      "type": "number",
      "title": "RA (degrees)",
      "default": 342.16
    },
    "dec": {
      "type": "number",
      "title": "dec (degrees)",
      "default": 33.94
    },
    "fov": {
      "type": "number",
      "title": "search radius (degrees)",
      "default": 10
    },
    "dataproduct_type": {
      "type": "string",
      "title": "DataProduct Type",
      "default": "all",
      "enum": ["all","image","cube"],
      "enumNames": ["all","image","cube"]
    },
    "dataproduct_subtype": {
      "type": "string",
      "title": "DataProduct Subtype",
      "default": "continuumMF",
      "enum": ["all","continuumMF","imageCube","beamCube"],
      "enumNames": ["all","continuumMF","imageCube","beamCube"]
    },
    "startdate": {
      "type": "string",
      "format" : "date",
      "title": "Start Date",
      "default": "2004-02-07"
    }
    ,
    "enddate": {
      "type": "string",
      "format" : "date",
      "title": "End Date",
      "default": "2004-02-08"
    },
    "instrument": {
      "type": "string",
      "title": "Instrument",
      "default": "eit"
    }
  }
}

