from .. import services, providers
from ..config import BASE_DIR
import os
import xml.etree.ElementTree as ET


def define_job(name: str) -> dict:
    job: dict = services.yaml.get_job(name)

    # replace key for better understanding of the result
    job["default_parameter_overrides"] = job.pop(
        "default_parameters", {})

    jobparams = job_available_parameters(job["path"])
    job["available_parameters"] = jobparams
    return job


def job_available_parameters(job_path: str) -> dict:
    job_path = os.path.join(BASE_DIR + "/jobs", job_path)
    tree = ET.parse(job_path)
    params = tree.findall("./parameters/parameter")
    result: list[dict] = []
    for param in params:
        result.append({
            'name': param.findtext("name"),
            'default': param.findtext("default_value"),
            'description': param.findtext("description")
        })
    return result


def get_executions(name):
    return providers.job.get_executions(name)


def get_execution(name, rowid):
    return providers.job.get_execution(name, rowid)


def execute(name: str, override_parameters: dict, id_secuence_execution: int = None):
    job = services.yaml.get_job(name)
    jobParameters = job["default_parameters"]
    if override_parameters is not None:
        jobParameters.update(override_parameters)
    return services.pdi.execute(name, job, jobParameters, id_secuence_execution)
