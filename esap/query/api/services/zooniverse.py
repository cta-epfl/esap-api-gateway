from .query_base import query_base
from panoptes_client import Panoptes, Project
from panoptes_client.panoptes import PanoptesAPIException
import logging

from esap.configuration.zooniverse_fields import workflow_fields, project_fields

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------------------------------


class panoptes_connector(query_base):
    """
    The connector to access the ALTA dataproducts dataset
    """

    # Initializer
    def __init__(self, url):
        self.url = url
        self.panoptes = None
        self.panoptes_user = None

    # construct a query for this type of service
    def construct_query(
        self, dataset, esap_query_params, translation_parameters, equinox
    ):
        where = ""
        errors = []
        query = ""

        # Attempt to connect to Panoptes

        if (
            self.panoptes is None
            and "panoptes_user" in esap_query_params
            and "panoptes_password" in esap_query_params
        ):
            try:
                self.panoptes = Panoptes.connect(
                    username=esap_query_params["panoptes_user"][0],
                    password=esap_query_params["panoptes_password"][0],
                )
                self.panoptes_user = esap_query_params["panoptes_user"][0]

            except PanoptesAPIException as e:
                errors.append(f"PanoptesAPIException: {e}")
        elif self.panoptes is None:
            errors.append("No username or password specified for Panoptes login.")
            return query, where, errors

        try:
            present_keys = set(
                ["catalog", "project_fields", "workflow_fields"]
            ).intersection(esap_query_params.keys())
            query = "&".join(
                [f"{key}={esap_query_params[key][0]}" for key in present_keys]
            )
        except Exception as e:
            errors.append(f"Error in construct_query: {e}")
        # projects, workflows, classifications...

        return query, where, errors

    def run_query(self, dataset, dataset_name, query):
        """
        Delegates to panoptes_client for queries.
        """
        try:
            tokens = dict((kv.split("=") for kv in query.split("&")))
            if tokens["catalog"] in ["zooniverse_projects", "zooniverse_workflows"]:
                query_type = tokens["catalog"].split("_")[1][:-1]
                query_fields_key = f"{query_type}_fields"
                have_query_fields_key = query_fields_key in tokens and tokens[query_fields_key]
                # Delegate retrieval to Panoptes API
                projects = Project.where(owner=self.panoptes_user)
                if "project" in query_type:
                    if have_query_fields_key:
                        query_fields = tokens[f"{query_type}_fields"].split(",")
                    else:
                        query_fields = project_fields()

                    results = [
                        dict(
                            [
                                ("display_name", project.display_name),
                                ("project_id", project.id),
                                ("created_at", project.raw["created_at"]),
                                ("updated_at", project.raw["updated_at"]),
                                ("slug", project.raw["slug"]),
                                ("live", project.raw["live"]),
                                (
                                    "available_languages",
                                    project.raw["available_languages"],
                                ),
                                ("launch_date", project.raw["launch_date"]),
                            ]
                            + [(field, project.raw[field]) for field in query_fields]
                        )
                        for project in projects
                    ]
                    return results
                # must be a workflow query
                if have_query_fields_key:
                    query_fields = tokens[f"{query_type}_fields"].split(",")
                else:
                    query_fields = workflow_fields()

                results = [
                    {
                        "project_id": project.id,
                        "display_name": project.display_name,
                        "workflows": [
                            dict(
                                [
                                    ("workflow_id", workflow.id),
                                    ("display_name", workflow.display_name),
                                    ("created_at", workflow.raw["created_at"]),
                                    ("updated_at", workflow.raw["updated_at"]),
                                ]
                                + [
                                    (field, workflow.raw[field])
                                    for field in query_fields
                                ]
                            )
                            for workflow in project.links.workflows
                        ],
                    }
                    for project in projects
                ]
                if len(results):
                    return results
                else:
                    return [query]

            else:
                return [query]
                # raise Exception("Unrecognised Panoptes Entity.")
        except Exception as error:
            record = {}
            record["query"] = query
            record["dataset"] = dataset.uri
            record["error"] = str(error)
            results = [record]
