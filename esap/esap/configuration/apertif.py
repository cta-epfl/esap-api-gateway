
# title = "ADEX"
logo = "https://alta.astron.nl/alta-static/images/esap/adex_logo.png"

# title = "ESFRI Science Analysis Platform"
# logo = "http://uilennest.net/static/media/tree9.da598501.png"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename = "adex-gui"

# definition of the navigation bar
nav1 = {'title': 'Archives', 'route': '/archives'}
nav2 = {'title': 'Query', 'route': '/query'}
navbar = [nav1, nav2]

# definition of the query
query_schema = {
    "name": "apertif",
    "title": "Apertif Data Collection Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "default": "apertif",
            "enum": ["adex", "apertif"],
            "enumNames": ["ADEX", "Apertif"],
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
        "collection": {
            "type": "string",
            "title": "Apertif Collections",
            "default": "imaging",
            "enum": ["imaging", "timedomain"],
            "enumNames": ["Imaging", "Timedomain"],
        },
        "level": {
            "type": "string",
            "title": "Processing Level",
            "default": "all",
            "enum": ["all", "raw", "processed"],
            "enumNames": ["All", "Raw", "Processed"]
        },
        "dataproduct_type": {
            "type": "string",
            "title": "DataProduct Type",
            "default": "all",
            "enum": ["all", "visibility", "image", "cube"],
            "enumNames": ["All", "Visibility", "Image", "Cube"]
        }
    }
}
