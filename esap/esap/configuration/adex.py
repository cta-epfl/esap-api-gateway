
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
    "name": "adex",
    "title": "ASTRON Data Collection Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "default": "adex",
            "enum": ["adex", "apertif", "astron_vo", "lofar"],
            "enumNames": ["All", "Apertif", "ASTRON_VO", "LOFAR"],
        },
        "target": {
            "type": "string",
            "title": "Target"
        },
        "ra": {
            "type": "number",
            "title": "RA (degrees)",
            "default": 342.16,
        },
        "dec": {
            "type": "number",
            "title": "dec (degrees)",
            "default": 33.94,
        },
        "fov": {
            "type": "number",
            "title": "search radius (degrees)",
            "default": 2.0,
        },
    },
}
