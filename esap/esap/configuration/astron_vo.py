logo = "https://alta.astron.nl/alta-static/images/esap/adex_logo.png"

# definition of the query
query_schema = {
    "name": "astron_vo",
    "title": "ASTRON VO Data Collection Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "default": "astron_vo",
            "enum": ["adex", "astron_vo"],
            "enumNames": ["ADEX", "ASTRON_VO"],
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
        "level": {
            "type": "string",
            "title": "Processing Level",
            "default": "processed",
            "enum": ["processed"],
            "enumNames": ["Processed"]
        },
        "collection": {
            "type": "string",
            "title": "Astron-VO Collections",
            "default": "apertif-dr1",
            "enum": ["apertif-dr1", "hetdex", "lotss-dr1", "lotss-pdr", "MSSSVerification", "sauron", "tgssadr"],
            "enumNames": ["apertif-dr1", "hetdex", "lotss-dr1", "lotss-pdr", "MSSSVerification", "sauron", "tgssadr"],
        },
    },
}
