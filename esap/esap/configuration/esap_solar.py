
title = "ESAP Solar"
logo = "https://alta.astron.nl/alta-static/images/esap/esap_solar.png"

# if datasets_enabled is set, then only these datasets are visible to the GUI
datasets_enabled = ['vso', 'helio']

# definition of the query
query_schema = {
    "title": "ESAP Solar Query",
    "type": "object",
    "properties": {
        "dataproduct_type": {
            "type": "string",
            "title": "DataProduct Type",
            "default": "all",
            "enum": ["all", "image", "cube"],
            "enumNames": ["all", "image", "cube"]
        },
        "startdate": {
            "type": "string",
            "format": "date",
            "title": "Start Date"
        },
        "enddate": {
            "type": "string",
            "format": "date",
            "title": "End Date"
        },
        "instrument": {
            "type": "string",
            "default": "SOHO__MDI",
            "enum": ["all", "SOHO__EIT", "SOHO__MDI", "PDMO__COGHA", "HINODE__EIS", "STEREO_A__COR", "STEREO_B__COR"],
        }
    }
}
