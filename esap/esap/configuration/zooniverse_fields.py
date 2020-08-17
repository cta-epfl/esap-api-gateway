from panoptes_client import Panoptes, Project, Workflow
from collections.abc import Iterable
import numpy as np

PAN = Panoptes.connect()

MANDATORY_PROJECT_FIELDS = [
    "id",
    "display_name",
    "created_at",
    "updated_at",
    "slug",
    "live",
    "available_languages",
    "launch_date",
]

MANDATORY_WORKFLOW_FIELDS = ["id", "display_name", "created_at", "updated_at"]


def is_or_contains_dict(item):
    if isinstance(item, dict):
        return True
    elif isinstance(item, Iterable):
        return np.any((is_or_contains_dict(element) for element in item))
    return False


def project_fields():
    projects = Project.where()
    project = next(iter(projects))
    fields = [
        key
        for key in set(project.raw.keys()).difference(MANDATORY_PROJECT_FIELDS)
        if type(project.raw[key]) is not dict
    ]

    return fields


def workflow_fields():
    workflows = Workflow.where()
    workflow = next(iter(workflows))
    fields = [
        key
        for key in set(workflow.raw.keys()).difference(MANDATORY_WORKFLOW_FIELDS)
        if type(workflow.raw[key]) is not dict
    ]
    return fields
