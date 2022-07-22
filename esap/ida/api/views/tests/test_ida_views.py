import json
from textwrap import indent
from django.core.exceptions import FieldError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

# from ida.api.services.tests.util import create_database_entry, assert_ok_error
from ida.api.views import SearchFacilities
from ida.models import Workflow


class CreateAndRunQueryViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # self.dataset_names = ["simba", "nala", "mufasa"]
        # self.dataset_list = [
        #     create_database_entry("apertif.alta_connector", self.dataset_names[0], "https://alta.astron.nl/altapi",
        #                           parameters="{\r\n\"collection\":\"collection\"\r\n}"),
        #     create_database_entry("astron_vo.tap_service_connector", self.dataset_names[1],
        #                           "https://vo.astron.nl/__system__/tap/run/tap", "ivoa.obscore",
        #                           "{\r\n\"collection\":\"obs_collection\"\r\n}"),
        #     create_database_entry("lofar.lta_connector", self.dataset_names[2], "https://lta.lofar.eu/",
        #                           parameters="{\r\n\"collection\":\"collection\"\r\n}")]

    def test_ida_view(self):
        # datasets = Workflow.objects.all()
        # self.assertEquals(len(datasets), 3)
        # self.assertEquals(self.dataset_list, list(datasets))

        url = reverse('workflows-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        print(json.dumps(response.json(), indent=4))
        # self.assertEquals(self.dataset_list, response.data['results'].serializer.instance)

#     def test_no_query_params(self):
#         url = reverse('query-view')  # equivalent to "/esap-api/query/query"
#         response = self.client.get(url)
#         assert_ok_error(self, response, "No query parameters given")

#     def test_unknown_dataset(self):
#         url = "/esap-api/query/query?dataset_uri=test"
#         response = self.client.get(url, follow=True)
#         assert_ok_error(self, response, "No datasets found for this query")

#     def test_unknown_archive(self):
#         url = "/esap-api/query/query?archive_uri=test"
#         response = self.client.get(url, follow=True)
#         assert_ok_error(self, response, "No datasets found for this query")

#     def test_filter_level(self):
#         for dataset_name in self.dataset_names:
#             # unknown
#             base_path = "/esap-api/query/query/?dataset_uri=%s&"
#             response = self.client.get(path=((base_path + "level=unknown") % dataset_name))
#             assert_ok_error(self, response, "No datasets found for this query")
#             # known
#             response = self.client.get(path=((base_path + "level=large") % dataset_name))
#             self.assertEqual(response.status_code, 200)
#             self.assertEquals(len(response.data['results']), 0, msg="wrong results for " + dataset_name)

#     def test_filter_category(self):
#         for dataset_name in self.dataset_names:
#             # unknown
#             base_path = "/esap-api/query/query/?dataset_uri=%s&"
#             response = self.client.get(path=((base_path + "category=unknown") % dataset_name))
#             assert_ok_error(self, response, "No datasets found for this query")
#             # known
#             response = self.client.get(path=((base_path + "category=lions") % dataset_name))
#             self.assertEqual(response.status_code, 200)
#             self.assertEquals(len(response.data['results']), 0, msg="wrong results for " + dataset_name)

#     def test_filter_collection(self):
#         for dataset_name in self.dataset_names:
#             base_path = "/esap-api/query/query/?dataset_uri=%s&"
#             # unknown
#             response = self.client.get(path=((base_path + "collection=unknown") % dataset_name))
#             assert_ok_error(self, response, "No datasets found for this query")
#             # known
#             response = self.client.get(
#                 path=((base_path + "collection=main character") % dataset_name))
#             self.assertEqual(response.status_code, 200)
#             if dataset_name == self.dataset_names[2]:  # lofar is not yet implemented therefore it is different
#                 self.assertEquals(len(response.data['results']), 19, msg="wrong results for " + dataset_name)
#             else:
#                 self.assertEquals(len(response.data['results']), 0, msg="wrong results for " + dataset_name)

#     def test_filter_archive_uri(self):
#         for dataset_name in self.dataset_names:
#             # unknown
#             base_path = "/esap-api/query/query/?dataset_uri=%s&"
#             response = self.client.get(path=((base_path + "archive_uri=unknown") % dataset_name))
#             assert_ok_error(self, response, "No datasets found for this query")
#             # known
#             response = self.client.get(path=((base_path + "archive_uri=lion-king") % dataset_name))
#             self.assertEqual(response.status_code, 200)
#             self.assertEquals(len(response.data['results']), 0, msg="wrong results for " + dataset_name)


# class ExtractAndFilterMethodTest(TestCase):
#     def setUp(self):
#         self.dataset_names = ["simba", "nala", "mufasa"]
#         self.dataset_list = [
#             create_database_entry("a", self.dataset_names[0], "b"),
#             create_database_entry("a", self.dataset_names[1], "b"),
#             create_database_entry("a", self.dataset_names[2], "b")]

#     def test_available_values(self):
#         query_params = {'archive_uri': ['lion-king'],
#                         'collection': ["main character"],
#                         'level': ['large'],
#                         'category': ['lions']}
#         all_datasets = common_views.get_datasets()
#         datasets, params = extract_and_filter(all_datasets, query_params, 'archive_uri', 'dataset_archive__uri')
#         self.assertEquals(self.dataset_list, list(datasets))
#         datasets, params = extract_and_filter(all_datasets, query_params, 'collection', 'collection')
#         self.assertEquals(self.dataset_list, list(datasets))
#         datasets, params = extract_and_filter(all_datasets, query_params, 'category', 'category')
#         self.assertEquals(self.dataset_list, list(datasets))
#         datasets, params = extract_and_filter(all_datasets, query_params, 'level', 'level')
#         self.assertEquals(self.dataset_list, list(datasets))

#     def test_keep_query_param_value(self):
#         query_params = {'collection': ["main character"],
#                         'category': ['lions']}
#         all_datasets = common_views.get_datasets()
#         datasets, params = extract_and_filter(all_datasets, query_params, 'collection', 'collection', False)
#         datasets, params = extract_and_filter(datasets, params, "category", "category")
#         self.assertEquals(len(params.keys()), 1)
#         self.assertIsNotNone(params.get("collection"))
#         self.assertIsNone(params.get("category"))

#     def test_raise_field_error(self):
#         query_params = {'test': ["value"]}
#         all_datasets = common_views.get_datasets()
#         with self.assertRaises(FieldError):
#             extract_and_filter(all_datasets, query_params, 'test', 'test')

#     def test_filter_datasets_with_resulting_datasets(self):
#         query_params = {'archive_uri': ['lion-king'],
#                         'collection': ["main character"],
#                         'level': ['large'],
#                         'category': ['lions']}
#         all_datasets = common_views.get_datasets()
#         datasets, params = filter_datasets(all_datasets, query_params)
#         self.assertEquals(self.dataset_list, list(datasets))
#         self.assertEquals(len(params.keys()), 1)
#         self.assertIsNotNone(params.get("collection"))

#     def test_filter_datasets_without_resulting_datasets(self):
#         query_params = {'collection': ['invalid']}
#         all_datasets = common_views.get_datasets()
#         datasets, params = filter_datasets(all_datasets, query_params)
#         self.assertEquals(len(datasets), 0)
