
# title = "ESFRI Science Analysis Platform"
#logo = "http://uilennest.net/static/media/tree9.da598501.png"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename="esap-gui"

logo = "https://alta.astron.nl/alta-static/images/esap/esap_logo.png"

# definition of the navigation bar
nav1 = {'title': 'Archives', 'route': '/archives'}
nav2 = {'title': 'Datasets', 'route': '/datasets'}
nav3 = {'title': 'Telescopes', 'route': '/telescopes'}
nav4 = {'title': 'Query', 'route': '/query'}
nav5 = {'title': 'Settings', 'route': '/about'}
navbar = [nav1,nav2,nav3,nav4,nav5]

# if datasets_enabled is set, then only these datasets are visible to the GUI
#datasets_enabled = ['apertif-observations','astron.ivoa.obscore']

# if datasets_disabled is set, then all datasets except these are returned to the GUI
datasets_disabled = ['nancay.ivoa.obscore']


# definition of the query
query_schema = {
  "title": "ESAP Query",
  "type": "object",
  "properties": {
    "institute": {
      "type": "string",
      "title": "Institute",
      "default": "all",
      "enum": ["all","Astron","IVOA"],
      "enumNames": ["all","astron","IVOA"]
    },
    "keyword": {
      "type": "string",
      "title": "Keyword",
      "default": ""
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
      "enum": ["all","image","cube","timeSeries","visibility"],
      "enumNames": ["all","image","cube","timeSeries","visibility"]
    },
    "dataproduct_subtype": {
      "type": "string",
      "title": "DataProduct Subtype",
      "default": "continuumMF",
      "enum": ["all", "uncalibratedVisibility", "calibrationTable", "continuumMF", "continuumChunk", "imageCube","beamCube", "calibratedImage", "polarisationImage", "polarisationCube", "pulsarTimingTimeSeries"],
      "enumNames": ["all", "uncalibratedVisibility", "calibrationTable", "continuumMF", "continuumChunk", "imageCube", "beamCube", "calibratedImage", "polarisationImage", "polarisationCube", "pulsarTimingTimeSeries"]
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
      "title": "Instrument",
      "default": "SOHO__MDI",
      "enum": ["all", "SOHO__EIT", "SOHO__MDI", "PDMO__COGHA", "HINODE__EIS", "STEREO_A__COR", "STEREO_B__COR"],
    }
  }
}
