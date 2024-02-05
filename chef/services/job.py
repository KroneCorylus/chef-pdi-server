from clases.job import Job
import services
import providers
from config import PDI_HOME
import os
import xml.etree.ElementTree as ET


def define_job(name: str) -> Job:
    job: Job = services.yaml.get_job(name)
    job.available_parameters = job_available_parameters(job.path)
    # job = redact_hidden_params(job)
    return job


def redact_hidden_params(job):
    params_to_be_redacted: list[str] = job.get("hidden_parameters", [])

    for key_to_redact in params_to_be_redacted:
        if (
            job.get("default_parameter_overwrites") is not None and
            job.get("default_parameter_overwrites").get(
                key_to_redact) is not None
        ):
            job.get("default_parameter_overwrites")[
                key_to_redact] = "***REDACTED***"
        for kjb_parameter in job.get("available_parameters", []):
            if kjb_parameter.get("name") == key_to_redact:
                kjb_parameter["default"] = "***REDACTED***"
    return job


def job_available_parameters(job_path: str) -> list[dict[str, str]]:
    job_path = os.path.join(PDI_HOME + "/jobs", job_path)
    xml_params = ET.parse(job_path).findall("./parameters/parameter")
    result: list[dict[str, str]] = []
    for xml_param in xml_params:
        param: dict[str, str] = {}
        param['name'] = xml_param.findtext("name", "")
        param['default'] = xml_param.findtext("default", "")
        param['description'] = xml_param.findtext("description", "")
        result.append(param)
    return result


def get_executions(name) -> list[dict]:
    return providers.job.get_executions(name)


def get_executions_by_secuence_id(id_secuence_execution: int) -> list[dict]:
    return providers.job.get_executions_by_secuence_execution(id_secuence_execution)


def get_execution(name, rowid):
    return providers.job.get_execution(name, rowid)


def execute(name: str,
            parameter_overwrites: dict,
            id_secuence_execution: int | None = None):
    job = services.yaml.get_job(name)
    jobParameters = job.parameter_overwrites
    if parameter_overwrites is not None:
        jobParameters.update(parameter_overwrites)
    return services.pdi.execute(name,
                                job,
                                jobParameters,
                                id_secuence_execution)
