
# definition of the IDA interface
ida_schema = {
    "name": "ida",
    "title": "Interactive Data Analysis",
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

    "required": ["compute"],

    "dependencies": {
        "compute": {
            "oneOf": [
                {
                    "properties": {
                        "compute": {"enum": ["jhub_uedin"]},
                        "interpreter": {
                            "type": "string",
                            "title": "Available Interpreter",
                            "default": "Python3.6",
                            "enum": ["vo_access", "ml_libs", "python3.6"],
                            "enumNames": ["VO Access", "ML Libs", "Python3.6"],
                            "uniqueItems": True,
                        },
                    },
                },
                {
                    "properties": {
                        "compute": {"enum": ["jhub_uedin"]},
                        "interpreter": {
                            "type": "string",
                            "title": "Available Interpreter",
                            "default": "default",
                            "enum": ["default", "data_science"],
                            "enumNames": ["Default", "Jupyter data science notebook"],
                            "uniqueItems": True,
                        },
                    }
                }
            ]
        },
    },
}
