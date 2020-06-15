"""
    File name: staging_base.py
    Author: Nico Vermaas & Zheng Meyer-Zhao - Astron
    Date created: 2020-03-09
    Description:  ESAP staging abstract base class.
"""

class staging_base:

    # Initializer
    def __init__(self, url):
        self.url = url

    # implement this in the derived service classes
    def construct_stage_request(self, dataset, esap_params, translation_mapping):
        pass

    # implement this in the derived service classes
    def run_stage_request(self, dataset):
        pass