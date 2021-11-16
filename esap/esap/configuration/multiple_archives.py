logo = "https://alta.astron.nl/alta-static/images/esap/esap_logo.png"

# which datasets are used for the multi archives query?
archives = ["apertif","astron_vo"]
#datasets_enabled = ["apertif-imaging-processeddata","apertif-timedomain-raw","astron_vo-apertif-dr1","lotss-dr1","sauron-hi-survey"]
datasets_enabled = [
    {"archive" : "apertif", "dataset": "apertif-imaging-rawdata"},
    {"archive" : "apertif", "dataset": "apertif-imaging-processeddata"},
    {"archive" : "apertif", "dataset": "apertif-timedomain-raw"},
    {"archive" : "astron_vo", "dataset": "astron_vo-apertif-dr1"},
    {"archive" : "astron_vo", "dataset": "tgssadr-image"},
    {"archive" : "astron_vo", "dataset": "lotss-dr1"},
    {"archive" : "astron_vo", "dataset": "lotss-pdr"},
    {"archive" : "astron_vo", "dataset": "hetdex"},
    {"archive" : "astron_vo", "dataset": "sauron-hi-survey"}
]

# definition of the query
query_schema = {
    "name": "multiple_archives",
    "title": "Multiple Archives Query",
    "type": "object",
    "properties": {

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
        "page_size": {
            "type": "number",
            "title": "results per dataset",
            "default": 10,
        },
    },
}
