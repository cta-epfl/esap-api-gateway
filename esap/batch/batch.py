
# definition of the IDA interface
batch_schema = {
    "name": "batch",
    "title": "Batch Analysis",
    "type": "object",
    "properties": {
        "compute": {
            "type": "string",
            "title": "Compute Facility",
            "default": "jhub_ska",
            "enum": ["jhub_ska", "jhub_uedin", "spark_uedin"],
            "enumNames": ["JHub SKA", "JHub Edinburgh", "Spark Cluster Edi"],
            "uniqueItems": True,
        },
    },
}
