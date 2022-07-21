settings = {
    "defaults": {
        "survey": "apertif_dr1",
        "color_map": "native",
        "ra": 340.0,
        "dec": 34.0,
        "fov": 15,
        "f_min": 10,
        "f_max": 1430,
        "pageSize": 1000,
        "refreshFactor": 0.5,
        # All available options for these lists
        "archives": ["lofar", "astron_vo", "apertif"],
        "calibration_levels": ["raw", "processed"],
        "dataproduct_types": ["image", "visibility", "cube", "timeSeries"],
        "collections": ["imaging", "timedomain", "lofar", "apertif-dr1", "sauron", "MSSSVerification", "tgssadr",
                        "lotss-dr1", "lotss-pdr"],
    },
    "surveys": [
        {
            "hips_name": "apertif_dr1",
            "hips_url": "https://hips.astron.nl/ASTRON/P/apertif_dr1",
            "format": "png"
        },
        {
            "hips_name": "lotss_dr1_low",
            "hips_url": "https://hips.astron.nl/ASTRON/P/lotss_dr1_low",
            "format": "png"
        },
        {
            "hips_name": "lotss_dr1_high",
            "hips_url": "https://hips.astron.nl/ASTRON/P/lotss_dr1_high",
            "format": "png"
        },
        {
            "hips_name": "tgssadr",
            "hips_url": "https://hips.astron.nl/ASTRON/P/tgssadr",
            "format": "png"
        },
        {
            "hips_name": "lotss_dr2_low",
            "hips_url": "https://hips.astron.nl/ASTRON/P/lotss_dr2_low",
            "format": "png"
        },
        {
            "hips_name": "lotss_dr2_high",
            "hips_url": "https://hips.astron.nl/ASTRON/P/lotss_dr2_high",
            "format": "png"
        },
    ],
    "color_maps": ["native", "grayscale", "cubehelix", "eosb", "rainbow"],
    "datasets": [
        {"lofar-lta": {
            "uri": "lofar-lta",
            "archive": "lofar",
            "collection": "lofar",
            "level": "raw",
            "dataproduct_type": "visibility",
            "freq_min": 10,
            "freq_max": 240
        }},
        {"astron_vo-apertif-dr1-cube": {
            "uri": "astron_vo-apertif-dr1",
            "archive": "astron_vo",
            "collection": "apertif-dr1",
            "level": "processed",  # = 3
            "dataproduct_type": "cube",
            "freq_min": 1338,
            "freq_max": 1415
        }},
        {"astron_vo-apertif-dr1-image": {
            "uri": "astron_vo-apertif-dr1",
            "archive": "astron_vo",
            "collection": "apertif-dr1",
            "level": "processed",  # = 3
            "dataproduct_type": "image",
            "freq_min": 1338,
            "freq_max": 1415
        }},
        {"sauron-hi-survey": {
            "uri": "sauron-hi-survey",
            "archive": "astron_vo",
            "collection": "sauron",
            "level": "processed",  # = 0
            "dataproduct_type": "image",
            "freq_min": 1410,
            "freq_max": 1430
        }},
        {"msss-verification": {
            "uri": "msss-verification",
            "archive": "astron_vo",
            "collection": "MSSSVerification",
            "level": "processed",  # = 0
            "dataproduct_type": "image",
            "freq_min": 30,
            "freq_max": 190
        }},
        {"tgssadr-image": {
            "uri": "tgssadr-image",
            "archive": "astron_vo",
            "collection": "tgssadr",
            "level": "processed",  # = 0
            "dataproduct_type": "image",
            "freq_min": 147,
            "freq_max": 147
        }},
        {"lotss-dr1": {
            "uri": "lotss-dr1",
            "archive": "astron_vo",
            "collection": "lotss-dr1",
            "level": "processed",  # = 3
            "dataproduct_type": "image",
            "freq_min": 120,
            "freq_max": 168
        }},
        {"lotss-pdr": {
            "uri": "lotss-pdr",
            "archive": "astron_vo",
            "collection": "lotss-pdr",
            "level": "processed",  # = 0
            "dataproduct_type": "image",
            "freq_min": 120,
            "freq_max": 168
        }},
        {"apertif-imaging-rawdata": {
            "uri": "apertif-imaging-rawdata",
            "archive": "apertif",
            "collection": "imaging",
            "level": "raw",  # = 0
            "dataproduct_type": "visibility",
            "freq_min": 1338,
            "freq_max": 1415
        }},
        {"apertif-imaging-processeddata-cube": {
            "uri": "apertif-imaging-processeddata",
            "archive": "apertif",
            "collection": "imaging",
            "level": "processed",  # = 1, 2,
            "dataproduct_type": "cube",
            "freq_min": 1338,
            "freq_max": 1415
        }},
        {"apertif-imaging-processeddata-image": {
            "uri": "apertif-imaging-processeddata",
            "archive": "apertif",
            "collection": "imaging",
            "level": "processed",  # = 1, 2,
            "dataproduct_type": "image",
            "freq_min": 1338,
            "freq_max": 1415
        }},
        {"apertif-imaging-processeddata-visibility": {
            "uri": "apertif-imaging-processeddata",
            "archive": "apertif",
            "collection": "imaging",
            "level": "processed",  # = 1, 2,
            "dataproduct_type": "visibility",
            "freq_min": 1338,
            "freq_max": 1415
        }},
        {"apertif-timedomain-raw": {
            "uri": "apertif-timedomain-raw",
            "archive": "apertif",
            "collection": "timedomain",
            "level": "raw",  # = 0
            "dataproduct_type": "timeSeries",
            "freq_min": 1338,
            "freq_max": 1415
        }},
        # currently there is this dataset in the VO but is does not result in any data
        # {"hetdex": {
        #     "archive": "astron_vo",
        #     "collection": "hetdex,
        #     "level": "processed",
        #     "dataproduct_type": [],
        # }},
    ],
}
