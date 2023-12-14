from pdiserver import services
import json


def execute(name: str) -> str:
    secuence = services.yaml.get_secuence(name)
    for secuence_job in secuence:
        job_name = secuence_job["job"]
        parameter_overwrites = secuence_job["parameter_overwrites"]
        job = services.yaml.get_job(job_name)
        print(job)
    return json.dumps(secuence)
