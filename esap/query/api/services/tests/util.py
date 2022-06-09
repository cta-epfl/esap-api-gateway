from query.models import DataSet, Archive, Catalog, ParameterMapping


def create_database_entry(service_connector, dataset_name, url=None, resource_name=None,
                          parameters="{\"startdate\":\"start\"}"):
    parameter_mapping = ParameterMapping(uri=service_connector.split(".")[0],
                                         parameters=parameters)
    parameter_mapping.save()
    catalog = Catalog.objects.create(uri="disney", name="disney", parameters=parameter_mapping, url=url)
    archive = Archive.objects.create(uri="lion-king", name="lion-king")
    dataset = DataSet.objects.create(uri=dataset_name,
                                     name=dataset_name,
                                     category="lions",
                                     level="large",
                                     collection="main character",
                                     resource_name=resource_name,
                                     dataset_catalog=catalog,
                                     dataset_archive=archive,
                                     service_connector=service_connector)

    return dataset


def assert_ok_error(test_reference, response, expected_message):
    test_reference.assertEqual(response.status_code, 200)
    test_reference.assertTrue("ERROR" in str(response.data) or "Error" in str(response.data))
    test_reference.assertIn(expected_message, str(response.data))
