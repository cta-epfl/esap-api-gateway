from .query_base import query_base
from panoptes_client import Panoptes, Project
from panoptes_client.panoptes import PanoptesAPIException
import logging

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

        query = str(
            esap_query_params["catalog"][0]
        )  # projects, workflows, classifications...
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
                errors.append(e)
        elif self.panoptes is None:
            raise Exception("No username or password specified for Panoptes login.")

        return query, where, errors

    def run_query(self, dataset, dataset_name, query):
        """
        Delegates to panoptes_client for queries.
        """
        try:
            if query in ["zooniverse_projects", "zooniverse_workflows"]:
                # Delegate retrieval to Panoptes API
                projects = Project.where(owner=self.panoptes_user)
                if "zooniverse_projects" in query:
                    results = [
                        {
                            "display_name": project.display_name,
                            "project_id": project.id,
                            "created_at": project.raw["created_at"],
                            "updated_at": project.raw["updated_at"],
                            "slug": project.raw["slug"],
                            "live": project.raw["live"],
                            "available_languages": project.raw["available_languages"],
                            "launch_date": project.raw["launch_date"],
                        }
                        for project in projects
                    ]
                    return results
                # must be a workflow query
                results = [
                    {
                        "project_id": project.id,
                        "display_name": project.display_name,
                        "workflows": [
                            {
                                "workflow_id": workflow.id,
                                "display_name": workflow.display_name,
                                "created_at": workflow.raw["created_at"],
                                "updated_at": workflow.raw["updated_at"],
                            }
                            for workflow in project.links.workflows
                        ],
                    }
                    for project in projects
                ]
                return results

            else:
                raise Exception("Unrecognised Panoptes Entity.")
        except Exception as error:
            record = {}
            record["query"] = query
            record["dataset"] = dataset.uri
            record["error"] = str(error)
            results = [record]
