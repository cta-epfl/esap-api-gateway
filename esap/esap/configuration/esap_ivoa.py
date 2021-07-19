logo = "https://alta.astron.nl/alta-static/images/esap/esap_logo.png"

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
                    "default": "apertif"
        },
        "service_type": {
            "type": "string",
            "title": "Service Type",
            "default": "tap",
            "enum": ["tap", "scs", "ssa", "sia"],
            "enumNames": ["TAP: Tables", "SCS: Cone Search", "SSA: Spectra", "SIA: Images"]
        },
        "waveband": {
            "type": "string",
            "title": "Waveband",
            "default": "all",
            "enum": ["all", "radio", "millimeter", "infrared", "optical", "uv", "euv", "x-ray", "gamma-ray"],
            "enumNames": ["All", "Radio", "Millimeter", "Nnfrared", "Optical", "UV", "EUV", "X-ray", "Gamma-ray"],
        },
    },

    "required": ["catalog", "service_type"],

    "dependencies": {
        "service_type": {
            "oneOf": [
                    {
                        "properties": {
                            "service_type": {"enum": ["tap"]},
                            "adql_query": {
                                "type": "string",
                                "title": "ADQL Query",
                                "default": "SELECT TOP 100 * from ivoa.obscore WHERE obs_collection='apertif-dr1' and dataproduct_subtype='continuum'",
                            },
                            "tap_schema": {
                                "type": "string",
                                "title": "TAP_SCHEMA",
                                "enum": ["TAP_SCHEMA.schemas", "TAP_SCHEMA.tables", "TAP_SCHEMA.columns"],
                            }

                        },
                    },
                {
                        "properties": {
                            "service_type": {"enum": ["scs"]},
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
                                "title": "Search Radius (degrees)",
                            },
                            "url": {
                                "type": "string",
                                "title": "Service URL",
                            }
                        }
                }
            ]
        },

    }
}

ui_schema = {
    "adql_query": {"ui:widget": "hidden"},
    "tap_schema": {"ui:widget": "hidden"},
    "ra": {"ui:widget": "hidden"},
    "dec": {"ui:widget": "hidden"},
    "fov": {"ui:widget": "hidden"},
    "url": {"ui:widget": "hidden"},
}
