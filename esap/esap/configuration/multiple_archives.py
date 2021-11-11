logo = "https://alta.astron.nl/alta-static/images/esap/esap_logo.png"

archives = ["apertif","astron_vo"]

# definition of the query
query_schema = {
    "name": "multiple_archives",
    "title": "Multiple Astronomy Archives Query (cone search)",
    "type": "object",
    "properties": {

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
