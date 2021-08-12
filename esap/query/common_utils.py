# common functionality for all apps (the query app is considered the 'core' app of ESAP)
import os, yaml

def get_json_from_yaml(yaml_path, model):
    """
    Read the contents of a 'model' from a configuration yaml
    This function return
    :param model:
    :param yaml_path: path to the yaml file
    :return: a list of 'fields' for the requested 'model' in json format
    """
    results = []

    with open(yaml_path, 'r') as stream:
        try:
            # print(yaml.safe_load(stream))
            list = yaml.safe_load(stream)

            # iterate through the json structure and gather the dicts for the requested model
            for item in list:
                if item['model'] == model:
                    result = item['fields']
                    results.append(result)

            return results

        except yaml.YAMLError as exc:
            print(exc)
            return None
