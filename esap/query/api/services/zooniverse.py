from rest_framework import serializers
from .query_base import query_base
from panoptes_client import Panoptes, Project, User
from panoptes_client.panoptes import PanoptesAPIException
import logging
import numpy as np

from esap.configuration.zooniverse_fields import workflow_fields, project_fields

logger = logging.getLogger(__name__)

AMP_REPLACEMENT = "__safe__amp__"

# --------------------------------------------------------------------------------------------------------------------


class panoptes_connector(query_base):
    """
    The connector to access the Zooniverse Panoptes dataset
    """

    class TypeToSerializerMap:

        map = {
            type(float): serializers.FloatField(),
            type(int): serializers.IntegerField(),
            type(str): serializers.CharField(),
            type(dict): serializers.DictField(),
            type(list): serializers.ListField(),
        }

        @classmethod
        def getFieldForType(cls, value):
            return cls.map.get(type(value), serializers.JSONField())

    #
    class CreateAndRunQuerySerializer(serializers.Serializer):
        """
        Custom serializer classes implement dynamic field definition based on
        the contents of the query passed to it.
        """

        def __init__(self, *args, **kwargs):

            self.example_result = kwargs.get("instance", [])[0]

            super().__init__(*args, **kwargs)

            self.fields.update(
                {
                    key: panoptes_connector.TypeToSerializerMap.getFieldForType(value)
                    for key, value in self.example_result.items()
                }
            )

    # Initializer
    def __init__(self, url):
        self.url = url
        self.panoptes = None
        self.panoptes_user = None
        self.projects = None
        self.pagination = "FALSE"

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
                ["catalog", "project_fields", "workflow_fields", "page"]
            ).intersection(esap_query_params.keys())
            query = AMP_REPLACEMENT.join(
                [f"{key}={esap_query_params[key][0]}" for key in present_keys]
            )
        except Exception as e:
            errors.append(f"Error in construct_query: {e}")
        # projects, workflows, classifications...

        return query, where, errors

    def run_query(
        self,
        dataset,
        dataset_name,
        query,
        session=None,
        override_access_url=None,
        override_service_type=None,
    ):
        """
        Delegates to panoptes_client for queries.
        """
        try:
            tokens = dict(
                (kv.split("=") for kv in query.replace(AMP_REPLACEMENT, "&").split("&"))
            )
            if tokens["catalog"] in ["zooniverse_projects", "zooniverse_workflows"]:
                query_type = tokens["catalog"].split("_")[1][:-1]
                query_fields_key = f"{query_type}_fields"
                have_query_fields_key = (
                    query_fields_key in tokens and tokens[query_fields_key]
                )

                # Delegate retrieval to Panoptes API
                if (
                    self.projects is not None
                    or self._get_projects_for_user() is not None
                ):
                    itemCount = len(self.projects)
                else:
                    itemCount = Project.where(
                        owner=self.panoptes_user, page_size=1
                    ).page_count
                pageSize = tokens.get("page_size", 5)
                numPages = int(np.ceil(itemCount / pageSize))
                resultPage = min(int(tokens.get("page", 1)), numPages)
                if self.projects is not None:
                    projects = self.projects[
                        (resultPage - 1) * pageSize : pageSize * (resultPage)
                    ]
                else:
                    projects = Project.where(
                        owner=self.panoptes_user, page=resultPage, page_size=pageSize
                    )

                if "project" in query_type:
                    if have_query_fields_key:
                        query_fields = tokens[f"{query_type}_fields"].split(",")
                    else:
                        query_fields = project_fields()

                    results = [
                        dict(
                            [
                                ("requested_page", resultPage),
                                ("pages", numPages),
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
                        for _, project in zip(range(pageSize), projects)
                    ]
                    if results is None or len(results) == 0:
                        raise Exception(
                            f"NoneType project results: resultPage = {resultPage}, pageSize = {pageSize}"
                        )
                    elif len(results):
                        return results
                    else:
                        raise Exception(
                            f"Zero length response for project query: {query}"
                        )
                # must be a workflow query
                if have_query_fields_key:
                    query_fields = tokens[f"{query_type}_fields"].split(",")
                else:
                    query_fields = workflow_fields()

                results = [
                    {
                        "project_id": project.id,
                        "display_name": project.display_name,
                        "requested_page": resultPage,
                        "pages": numPages,
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
                    for _, project in zip(range(pageSize), projects)
                ]
                if results is None:
                    raise Exception(
                        f"NoneType project results: resultPage = {resultPage}, pageSize = {pageSize}"
                    )
                elif len(results):
                    return results
                else:
                    raise Exception(f"Zero length response for workflow query: {query}")
            else:
                raise Exception(f"Unreconised Zooniverse catalogue in query: {query}")
        except Exception as error:
            record = {}
            record["query"] = query
            record["dataset"] = dataset.uri
            record["error"] = str(error)
            results = [record]
            return results

    def _get_project_by_id(self, pid):
        try:
            return Project.find(pid)
        except PanoptesAPIException as e:
            return None

    def _get_projects_for_user(self):
        if self.panoptes_user is None:
            return None

        try:
            panoptes_user_obj = next(User.where(login=self.panoptes_user))
            project_role_response = self.panoptes.get(
                "/project_roles",
                params={"user_id": panoptes_user_obj.id, "page_size": 1000},
            )
            if not project_role_response:
                return None
            self.projects = [
                project
                for project in [
                    self._get_project_by_id(project_role_data["links"]["project"])
                    for project_role_data in project_role_response[0]["project_roles"]
                ]
                if project is not None
            ]
            return self.projects
        except StopIteration:
            return None
        except PanoptesAPIException:
            return None
