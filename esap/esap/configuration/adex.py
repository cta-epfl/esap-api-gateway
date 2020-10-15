
# title = "ADEX"
logo = "https://alta.astron.nl/alta-static/images/esap/adex_logo.png"

# title = "ESFRI Science Analysis Platform"
# logo = "http://uilennest.net/static/media/tree9.da598501.png"

# the url location of the frontend application,
# this makes it possible to install multiple instances in different directories on the webserver
# that all have their own urls like 'http://esap.astron.nl/esap-gui-dev/queries'
frontend_basename = "adex-gui"

# definition of the navigation bar
nav1 = {'title': 'Archives', 'route': '/archives'}
nav2 = {'title': 'Query', 'route': '/query'}
navbar = [nav1, nav2]


# definition of the query
query_schema = {
    "name": "adex",
    "title": "ASTRON Data Collection Query",
    "type": "object",
    "properties": {
        "catalog": {
            "type": "string",
            "title": "Catalog",
            "default": "astron_vo",
            "enum": ["apertif", "astron_vo", "lofar"],
            "enumNames": ["Apertif", "ASTRON_VO", "LOFAR"],
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
    },

    "required": ["catalog"],

    "dependencies": {
        "catalog": {
            "oneOf": [
                {
                    "properties": {
                        "catalog": {"enum": ["apertif"]},
                        "level": {
                            "type": "string",
                            "title": "Processing Level",
                            "default": "all",
                            "enum": ["all", "raw", "processed"],
                            "enumNames": ["All", "Raw", "Processed"]
                        },
                        "collection": {
                            "type": "string",
                            "title": "Apertif Collections",
                            "default": "imaging",
                            "enum": ["imaging", "timedomain"],
                            "enumNames": ["Imaging", "Timedomain"],        "ref_system": {
                                "type": "string",
                                "title": "Reference system",
                                "default": "J2000",
                                "enum": ["J2000", "B1950", "SUN", "JUPITER"],
                            },
                            "fov": {
                                "type": "number",
                                "title": "Search radius",
                            },
                            "fov_units": {
                                "type": "string",
                                "title": "Search Radius Units",
                                "default": "deg",
                                "enum": ["rad", "deg", "arcmin", "arcsec"],
                            },
                            "antenna_type": {
                                "type": "string",
                                "title": "Antenna Type",
                                "default": "HBA",
                                "enum": ["HBA", "LBA", "all"],
                                "enumNames": ["HBA", "LBA", "All"],
                            },
                            "public": {
                                "type": "boolean",
                                "title": "Public data only",
                                "default": True,
                                "enum": [True, False],
                            },
                            "sasid": {
                                "type": "string",
                                "title": "SAS Id",

                            },
                            "dataproduct_type": {
                                "type": "string",
                                "title": "Data Product Type",
                                "default": "AveragingPipeline",
                                "enum": ["CorrelatedDataProduct", "AveragingPipeline", "CalibrationPipeline", "ImagingPipeline", "LongBaselinePipeline", "PulsarPipeline"],
                                "enumNames": ["Observation", "Averaging Pipeline", "Calibration Pipeline", "Imaging Pipeline", "Long Baseline Pipeline", "Pulsar Pipeline"],
                            },
                        },

                    },
                    "dataproduct_type": {
                        "type": "string",
                        "title": "DataProductType",
                        "default": "all",
                        "enum": ["all", "visibility", "image", "cube"],
                        "enumNames": ["All", "Visibility", "Image", "Cube"]
                    },
                    #    "dataproduct_subtype": {
                    #      "type": "string",
                    #      "title": "DataProduct Type",
                    #      "default": "continuumMF",
                    #      "enum": ["all", "uncalibratedVisibility", "continuumMF", "continuumChunk", "calibratedImage", "polarisationImage",
                    #               "imageCube", "beamCube", "polarisationCube", "pulsarTimingTimeSeries"],
                    #      "enumNames": ["all", "uncalibratedVisibility", "continuumMF", "continuumChunk", "calibratedImage",
                    #                    "polarisationImage", "imageCube", "beamCube", "polarisationCube", "pulsarTimingTimeSeries"]
                    #    },
                },

                {
                    "properties": {
                        "catalog": {"enum": ["astron_vo"]},
                        "level": {
                            "type": "string",
                            "title": "Processing Level",
                            "default": "processed",
                            "enum": ["processed"],
                            "enumNames": ["Processed"]
                        },
                        "collection": {
                            "type": "array",
                            "title": "Astron-VO Collections",
                            "items": {
                                "type": "string",
                                "enum": ["hetdex", "lotss-dr1", "lotss-pdr", "MSSSVerification", "sauron", "tgssadr"],
                            },
                            "uniqueItems": True,
                        },
                    }
                },

                {
                    "properties": {
                        "catalog": {"enum": ["lofar"]},
                        "ref_system": {
                            "type": "string",
                            "title": "Reference system",
                            "default": "J2000",
                            "enum": ["J2000", "B1950", "SUN", "JUPITER"],
                        },
                        "fov": {
                            "type": "number",
                            "title": "Search radius",
                        },
                        "fov_units": {
                            "type": "string",
                            "title": "Search Radius Units",
                            "default": "deg",
                            "enum": ["rad", "deg", "arcmin", "arcsec"],
                        },
                        "antenna_type": {
                            "type": "string",
                            "title": "Antenna Type",
                            "default": "HBA",
                            "enum": ["HBA", "LBA", "all"],
                            "enumNames": ["HBA", "LBA", "All"],
                        },
                        "public": {
                            "type": "boolean",
                            "title": "Public data only",
                            "default": True,
                            "enum": [True, False],
                        },
                        "sasid": {
                            "type": "string",
                            "title": "SAS Id",

                        },
                        "dataproduct_type": {
                            "type": "string",
                            "title": "Data Product Type",
                            "default": "AveragingPipeline",
                            "enum": ["CorrelatedDataProduct", "AveragingPipeline", "CalibrationPipeline", "ImagingPipeline", "LongBaselinePipeline", "PulsarPipeline"],
                            "enumNames": ["Observation", "Averaging Pipeline", "Calibration Pipeline", "Imaging Pipeline", "Long Baseline Pipeline", "Pulsar Pipeline"],
                        },
                    }
                }
            ],
        },
    },
}

ui_schema = {
    "public": {
        "ui:widget": "radio",
    },
}
