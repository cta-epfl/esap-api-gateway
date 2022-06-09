from django.test import TestCase
from rest_framework.test import APIClient

from query.api.services.tests.util import create_database_entry, assert_ok_error


class CreateAndRunQueryTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_invalid_service_connector(self):
        dataset_name = "simba"
        create_database_entry("invalid.connector", dataset_name)

        response = self.client.get(path=("/esap-api/query/query/?dataset_uri=%s" % dataset_name))
        assert_ok_error(self, response, "No connector class found for service module")

    def test_missing_catalog_url_different_connectors(self):
        dataset_name_one = "mufasa"
        create_database_entry("apertif.alta_connector", dataset_name_one)

        dataset_name_two = "sarabi"
        create_database_entry("astron_vo.tap_service_connector", dataset_name_two)

        response = self.client.get(path=("/esap-api/query/query/?dataset_uri=%s" % dataset_name_one))
        assert_ok_error(self, response, "No catalog url found for catalog")
        response = self.client.get(path=("/esap-api/query/query/?dataset_uri=%s" % dataset_name_two))
        assert_ok_error(self, response, "No catalog url found for catalog")

    def test_missing_catalog_parameters(self):
        dataset_name = "nala"
        create_database_entry("some.connector", dataset_name, parameters=None)

        response = self.client.get(path="/esap-api/query/query/?dataset_uri=%s" % dataset_name)
        assert_ok_error(self, response, "No translation parameters found for catalog")

    def test_faulty_catalog_parameters(self):
        dataset_name = "nala"
        create_database_entry("some.connector", dataset_name, parameters="faulty")

        response = self.client.get(path="/esap-api/query/query/?dataset_uri=%s" % dataset_name)
        assert_ok_error(self, response, "Could not load the parameter mapping")