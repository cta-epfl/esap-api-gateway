
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
            "default": "A2255",
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
            "default": "HBA",
            "enum": ["HBA", "LBA", "all"],
            "enumNames": ["HBA", "LBA", "All"],
        },
        "public": {
            "type": "boolean",
            "title": "Public data only",
            "default": True,
            "enum": [True, False],
        },
        "sasid": {
            "type": "string",
            "title": "SAS Id",

        },
        "dataproduct_type": {
            "type": "string",
            "title": "Data Product Type",
            "default": "AveragingPipeline",
            "enum": ["CorrelatedDataProduct", "AveragingPipeline", "CalibrationPipeline", "ImagingPipeline", "LongBaselinePipeline", "PulsarPipeline"],
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
    "public": {
        "ui:widget": "radio",
    },
}
