
# title = "ESFRI Science Analysis Platform"
#logo = "http://uilennest.net/static/media/tree9.da598501.png"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename = "esap-gui"

logo = "https://alta.astron.nl/alta-static/images/esap/esap_logo.png"

# definition of the navigation bar
nav1 = {'title': 'Archives', 'route': '/archives'}
nav2 = {'title': 'Query', 'route': '/query'}
nav3 = {'title': 'Rucio', 'route': '/rucio'}
nav4 = {'title': 'Interactive Analysis', 'route': '/interactive'}
navbar = [nav1, nav2, nav3, nav4]

# if datasets_enabled is set, then only these datasets are visible to the GUI
#datasets_enabled = ['apertif-observations','astron.ivoa.obscore']

# if datasets_disabled is set, then all datasets except these are returned to the GUI
datasets_disabled = ['nancay.ivoa.obscore']


# definition of the query
query_schema = {
    "name": "ivoa",
    "title": "ESAP IVOA Query",
    "type": "object",
    "properties": {
        "service_type": {
            "type": "string",
            "title": "Service",
            "default": "tap",
            "enum": ["tap", "scs", "ssa", "sia"],
            "enumNames": ["TAP: Tables", "SCS: Cone Search", "SSA: Spectra", "SIA: Images"]
        },
        "keyword": {
            "type": "string",
            "title": "Keyword",
            "default": ""
        },

        # hidden property, keep it at the end of the properties list
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "default": "vo_reg",
            "enum": ["vo_reg"],
            "enumNames": ["IVOA"],
        },
    }
}

ui_schema = {"catalog": {"ui:widget": "hidden"}}
