from config import PDI_HOME, JOBS_FILE, SECUENCES_FILE
import yaml as __yaml


def load_yaml(path: str) -> dict:
    with open(PDI_HOME + path, 'r') as stream:
        return __yaml.safe_load(stream)


def get_jobs() -> dict:
    try:
        job_conf = load_yaml("/jobs/" + JOBS_FILE)
    except Exception as err:
        raise Exception("Configuration file for jobs not found.") from err
    result = job_conf.get("jobs")
    if result is None:
        raise Exception(
            "Missing jobs property on configuration file jobs.yaml.")
    return result


def get_job(name: str) -> dict:
    return get_jobs()[name]


def get_secuences() -> dict:
    return load_yaml("/jobs/" + SECUENCES_FILE)["secuences"]


def get_secuence(name: str) -> dict:
    return get_secuences()[name]
