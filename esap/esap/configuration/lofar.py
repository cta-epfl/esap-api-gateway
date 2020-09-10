
# title = "ADEX"
logo = "https://alta.astron.nl/alta-static/images/esap/adex_logo.png"

# title = "ESFRI Science Analysis Platform"
# logo = "http://uilennest.net/static/media/tree9.da598501.png"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename = "esap-gui"

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
    "name": "lofar",
    "title": "LOFAR LTA Data Collection Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "default": "lofar",
            "enum": ["lofar"],
            "enumNames": ["LOFAR"],
        },
        "target": {
            "type": "string",
            "title": "Object",
            "default": "",
        },
        "resolve": {
            "type": "boolean",
            "title": "Resolve RA and Dec",
            "enum": ["true", "false"],
        },
        "ra": {
            "type": "number",
            "title": "RA",
        },
        "dec": {
            "type": "number",
            "title": "Dec",
        },
        "units": {
            "type": "string",
            "title": "Units",
            "default": "sexagesimal",
            "enum": ["rad", "deg", "sexagesimal"],
        },
        "ref_system": {
            "type": "string",
            "title": "Reference system",
            "default": "J2000",
            "enum": ["J2000", "B1950", "SUN", "JUPITER"],
        },
        "fov": {
            "type": "number",
            "title": "Search radius",
            "default": "1.0"
        },
        "fov_units": {
            "type": "string",
            "title": "Search Radius Units",
            "default": "deg",
            "enum": ["rad", "deg", "arcmin", "arcsec"],
        },
        "antenna_type": {
            "type": "string",
            "title": "Antenna Type",
            "default": "all",
            "enum": ["hba", "lba", "all"],
            "enumNames": ["HBA", "LBA", "All"],
        },
        "public": {
            "type": "boolean",
            "title": "Public data only",
            "default": "true",
            "enum": ["true", "false"],
        },
        "sasid": {
            "type": "string",
            "title": "SAS Id",

        },
        "dataproduct_type": {
            "type": "string",
            "title": "Data Product Type",
            "default": "observation",
            "enum": ["observation", "averaging", "calibration", "imaging", "longbaseline", "pulsar"],
            "enumNames": ["Observation", "Averaging Pipeline", "Calibration Pipeline", "Imaging Pipeline", "Long Baseline Pipeline", "Pulsar Pipeline"],
        },
    },

    "required": ["catalog", "dataproduct_type"],

    "dependencies": {
        "dataproduct_type": {
            "oneOf": [
                {
                    "properties": {
                        "dataproduct_type": {"enum": ["observation"]},
                        "observing_mode": {
                            "type": "string",
                            "title": "Observing Mode",
                            "default": "all",
                            "enum": ["all", "imaging", "timedomain"],
                            "enumNames": ["All", "Imaging", "Time Domain"],
                            "uniqueItems": True,
                        },
                    },
                },
                {
                    "properties": {
                        "dataproduct_type": {"enum": ["pulsar"]},
                        "data_type": {
                            "type": "string",
                            "title": "Data Type",
                            "default": "all",
                            "enum": ["coherent", "incoherent", "flys_eye", "all"],
                            "enumNames": ["Coherent Stokes", "Incoherent Stokes", "Fly's Eye", "All"],
                        },
                    }
                }
            ]
        },
    },
}

ui_schema = {
    "resolve": {
        "ui:widget": "radio",
    },
    "public": {
        "ui:widget": "radio",
    },
}
