
logo = "https://alta.astron.nl/alta-static/images/esap/adex_logo.png"

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
            "default": "processed",
            "enum": ["raw", "processed"],
            "enumNames": ["Raw", "Processed"]
        },
        "dataproduct_type": {
            "type": "string",
            "title": "DataProduct Type",
            "default": "all",
            "enum": ["all", "visibility", "image", "cube"],
            "enumNames": ["All", "Visibility", "Image", "Cube"]
        },
        "release__release_id": {
            "type": "string",
            "title": "Data Release",
            "default": "APERTIF_DR1_Imaging",
            "enum": ["all", "APERTIF_DR1_Imaging", "SVC_2019_Imaging", "SVC_2019_TimeDomain", "Commissioning2018"],
            "enumNames": ["All", "APERTIF Imaging Data Release 1", "Science Verification Campaign 2019 (Imaging)", "Science Verification Campaign 2019 (Time Domain)", "Commissioning 2018"]
        },
    }
}
