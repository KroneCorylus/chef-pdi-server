from .. import services, providers
import json
import threading


def execute(name: str) -> str:
    secuence = services.yaml.get_secuence(name)
    id_secuence_execution = providers.secuence.insert(name)
    thread = threading.Thread(
        target=execute_jobs_in_secuence, args=(secuence, id_secuence_execution))
    thread.start()
    return json.dumps(secuence)


def execute_jobs_in_secuence(secuence: dict, id_secuence_execution: int):
    for job in secuence:
        job_name = job["job"]
        parameter_overwrites = job["parameter_overwrites"]
        services.job.execute(
            job_name, parameter_overwrites, id_secuence_execution)
    providers.secuence.update_end_date(id_secuence_execution)


def get_executions(name: str) -> list[dict]:
    return providers.secuence.get_executions(name)
