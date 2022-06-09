from django.test import TestCase
from rest_framework.test import APIClient

from query.api.services.tests.util import create_database_entry, assert_ok_error
from query.models import DataSet, Archive, Catalog, ParameterMapping


class AltaConnectorTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # mock-up data
        create_database_entry("apertif.alta_connector", "simba", "https://alta.astron.nl/altapi")
        # real data
        parameter_mapping = ParameterMapping(uri="apertif",
                                             parameters="{\r\n\"dataproduct_level\" : \"calibrationLevel\","
                                                        "\r\n\"dataproduct_type\" : \"dataProductType\","
                                                        "\r\n\"dataproduct_subtype\" : \"dataProductSubType\"\r\n}")
        parameter_mapping.save()
        catalog = Catalog.objects.create(uri="alta", name="ALTA Imaging raw data", parameters=parameter_mapping,
                                         url="https://alta.astron.nl/altapi")
        archive = Archive.objects.create(uri="apertif", name="WSRT-Apertif")
        DataSet.objects.create(uri="apertif-imaging-rawdata",
                               name="Imaging Survey raw data",
                               category="imaging",
                               level="raw",
                               collection="imaging",
                               dataset_catalog=catalog,
                               dataset_archive=archive,
                               service_connector="apertif.alta_connector")

        # if data is added, this might change
        self.alta_count = 16336

    def test_dataset_does_not_exist(self):
        url = "/esap-api/query/query?dataset_uri=simba"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.data['results']), 0)

    def test_dataset_exist(self):
        url = "/esap-api/query/query?dataset_uri=apertif-imaging-rawdata"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['count'], self.alta_count)

    def test_archive_has_no_data(self):
        url = "/esap-api/query/query?archive_uri=lion-king"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.data['results']), 0)

    def test_archive_exists(self):
        url = "/esap-api/query/query?archive_uri=apertif"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['count'],
                          self.alta_count)  # since only one real dataset is registered for this test

    def test_unknown_query_param_gives_error(self):
        url = "/esap-api/query/query?unknown_param_name=some-value&dataset_uri=apertif-imaging-rawdata"
        response = self.client.get(url, follow=True)
        assert_ok_error(self, response, "could not translate key")


class TapServiceConnectorTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # mock-up data
        create_database_entry("astron_vo.tap_service_connector", "simba", "https://vo.astron.nl/__system__/tap/run/tap",
                              "ivoa.obscore", "{\r\n\"collection\":\"obs_collection\"\r\n}")
        # real data
        create_database_entry("astron_vo.tap_service_connector", "lotss-dr1",
                              "https://vo.astron.nl/__system__/tap/run/tap",
                              "ivoa.obscore", "{\r\n\"collection\":\"obs_collection\"\r\n}")

        # this might change if pagination is changed
        self.astron_vo_count = 290

    def test_without_resource_name(self):
        create_database_entry("astron_vo.tap_service_connector", "nala", "https://vo.astron.nl/__system__/tap/run/tap")
        url = "/esap-api/query/query?dataset_uri=nala"
        response = self.client.get(url, follow=True)
        assert_ok_error(self, response, "No resource_name defined")

    def test_dataset_does_not_exist(self):
        url = "/esap-api/query/query?dataset_uri=simba"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.data['results']), 0)

    def test_dataset_exist(self):
        url = "/esap-api/query/query?dataset_uri=lotss-dr1"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['count'], self.astron_vo_count)

    def test_archive_exists(self):
        url = "/esap-api/query/query?archive_uri=lion-king"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['count'], self.astron_vo_count)

    def test_unknown_query_param_gives_error(self):
        url = "/esap-api/query/query?unknown_param_name=some-value&dataset_uri=lotss-dr1"
        response = self.client.get(url, follow=True)
        assert_ok_error(self, response, "Field query: No such field known")


class LtaConnectorTest(TestCase):
    # as soon as lofar is actually queried, these tests should be altered
    # now you can only query the fake data if you add parameters specifically for the lofar query

    def setUp(self):
        self.client = APIClient()
        # mock-up data
        create_database_entry("lofar.lta_connector", "simba", "https://lta.lofar.eu/")

        # this will change when we actually retrieve results
        self.lofar_count = 19

    def test_basic_query_gives_no_data(self):
        url = "/esap-api/query/query?dataset_uri=simba"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.data['results']), 0)

    def test_specified_query_gives_data(self):
        url = "/esap-api/query/query?dataset_uri=simba&startdate=10"
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['count'], self.lofar_count)

    def test_unknown_query_param_gives_error(self):
        url = "/esap-api/query/query?unknown_param_name=some-value&dataset_uri=simba"
        response = self.client.get(url, follow=True)
        assert_ok_error(self, response, "could not translate key")
