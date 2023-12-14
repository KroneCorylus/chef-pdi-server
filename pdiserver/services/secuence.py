from pdiserver import services
import json


def execute(name: str) -> str:
    secuence = services.yaml.get_secuence(name)
    for job in secuence:
        job_name = job["job"]
        parameter_overwrites = job["parameter_overwrites"]
        services.job.execute(job_name, parameter_overwrites, 1)
    return json.dumps(secuence)
