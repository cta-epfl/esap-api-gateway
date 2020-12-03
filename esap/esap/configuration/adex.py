logo = "https://alta.astron.nl/alta-static/images/esap/adex_logo.png"


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
