
title = "ESAP Solar"

frontend_basename="esap-solar"

logo = "https://alta.astron.nl/alta-static/images/esap/esap_solar.png"

# definition of the navigation bar
nav4 = {'title': 'Query', 'route': '/query'}
nav5 = {'title': 'Settings', 'route': '/about'}
navbar = [nav4,nav5]

# definition of the query
query_schema = {
  "title": "ESAP Solar Query",
  "type": "object",
  "properties": {
    "institute": {
      "type": "string",
      "title": "Institute",
      "default": "all",
      "enum": ["all","Astron"],
      "enumNames": ["all","astron"]
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
      "default": "all",
      "enum": ["all","continuumMF","imageCube","beamCube"],
      "enumNames": ["all","continuumMF","imageCube","beamCube"]
    },
    "startdate": {
      "type": "string",
      "format" : "date",
      "title": "Start Date"
    }
    ,
    "enddate": {
      "type": "string",
      "format" : "date",
      "title": "End Date"
    },
    "instrument": {
      "type": "string",
      "title": "Instrument"
    }
  }
}

