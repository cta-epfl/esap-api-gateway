logo = "https://alta.astron.nl/alta-static/images/esap/adex_logo_clear.png"

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
            "enum": ["apertif"],
            "enumNames": ["Apertif"],
        },
        "target": {
            "type": "string",
            "title": "Target"
        },
        "resolve": {
            "type": "boolean",
            "title": "Resolve Coordinates",
            "default": True,
            "enum": [True, False],
        },
        "ra": {
            "type": "number",
            "title": "RA",
        },
        "dec": {
            "type": "number",
            "title": "dec",
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
            "enum": ["J2000", "B1950", "SUN", "JUPITER", "GalacticCoord"],
            "enumNames": ["J2000", "B1950", "SUN", "JUPITER", "Galactic coordinates"],
        },
        "fov": {
            "type": "number",
            "title": "Search radius",
            "default": 0.75,
        },
        "fov_units": {
            "type": "string",
            "title": "Search Radius Units",
            "default": "deg",
            "enum": ["rad", "deg", "arcmin", "arcsec"],
        },
        "obs_date_start": {
            "type": "string",
            "title": "Observing date (start)",
        },
        "obs_date_end": {
            "type": "string",
            "title": "Observing date (end)",
        },
        "collection": {
            "type": "string",
            "title": "Observing mode",
            "default": "all",
            "enum": ["all", "imaging", "timedomain"],
            "enumNames": ["All", "Imaging", "Timedomain"],
        },
    },
    "dependencies": {
        "collection": {
            "oneOf": [
                {
                    "properties": {
                        "collection": {"enum": ["imaging"]},
                        "dataproduct_type": {
                            "type": "array",
                            "title": "Data product type",
                            "items": {
                                "type": "string",
                                "enum": ["all", "raw", "uv-calibrated", "continuumMF", "HI_cube", "Polarization_cube"],
                                "enumNames": ["All", "Raw Imaging data", "Uv-calibrated data", "continuum MF images", "HI cube", "Polarization cube"],
                            },
                            "uniqueItems": True,
                        },
                    },
                },
                {
                    "properties": {
                        "collection": {"enum": ["timedomain"]},
                        "dataproduct    _type": {
                            "type": "string",
                            "title": "Data Product Type",
                            "default": "all",
                            "enum": ["all", "coherent", "incoherent", "pulsartiming"],
                            "enumNames": ["All",    "Coherent Stokes time series data", "Incoherent Stokes time series data", "Pulsar timing data"],
                        },
                    }
                }
            ]
        },
    },
}

ui_schema = {
    "resolve": {
        "ui:widget": "checkbox",
    },
    "obs_date_start": {
        "ui:widget": "date",
    },
    "obs_date_end": {
        "ui:widget": "date",
    },
}
