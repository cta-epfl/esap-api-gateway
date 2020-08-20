
# title = "ESFRI Science Analysis Platform"
# logo = "http://uilennest.net/static/media/tree9.da598501.png"

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
# datasets_enabled = ['apertif-observations','astron.ivoa.obscore']

# if datasets_disabled is set, then all datasets except these are returned to the GUI
datasets_disabled = ['nancay.ivoa.obscore']


# definition of the query
query_schema = {
    "name": "ivoa",
    "title": "ESAP IVOA Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "default": "vo_reg",
            "enum": ["vo_reg"],
            "enumNames": ["IVOA"],
        },
        "keyword": {
            "type": "string",
                    "title": "Keyword",
                    "default": "UKIDSS"
        },
        "service_type": {
            "type": "string",
            "title": "Service Type",
            "default": "tap",
            "enum": ["tap", "scs", "ssa", "sia"],
            "enumNames": ["TAP: Tables", "SCS: Cone Search", "SSA: Spectra", "SIA: Images"]
        },
    },

    "required": ["catalog", "service_type"],


    # "service_type": {
    #     "oneOf": [
    #         {
    #             "properties": {
    #                 "service_type": {"enum": ["tap"]},
    #                 "adql_query": {
    #                     "type": "string",
    #                     "title": "ADQL Query",
    #                 },
    #                 "tap_schema": {
    #                     "type": "string",
    #                     "title": "TAP_SCHEMA",
    #                     "enum": ["TAP_SCHEMA.schemas", "TAP_SCHEMA.tables", "TAP_SCHEMA.columns"],
    #                 }
    #             },
    #         },
    #         {
    #             "properties": {
    #                 "service_type": {"enum": ["scs"]},
    #                 "ra": {
    #                     "type": "number",
    #                     "title": "RA (degrees)",
    #                 },
    #                 "dec": {
    #                     "type": "number",
    #                     "title": "dec (degrees)",
    #                 },
    #                 "fov": {
    #                     "type": "number",
    #                     "title": "Search Radius (degrees)",
    #                 },
    #                 "url": {
    #                     "type": "string",
    #                     "title": "Service URL",
    #                 }
    #             }
    #         }
    #     ]
    # },


}

ui_schema = {
    "adql_query": {"ui:widget": "textarea"},
}
