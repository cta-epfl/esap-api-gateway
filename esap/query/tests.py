from django.test import TestCase
import unittest

# Create your tests here.
from .api.services.ivoa import vo_registry_connector


class RegSearchTest(unittest.TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    # def test_registry_keyword_search(self):
    #     voreg = vo_registry_connector("")
    #     wsa_services = voreg.search(keywords=["wsa"])
    #     self.assertTrue(len(wsa_services)>0)
