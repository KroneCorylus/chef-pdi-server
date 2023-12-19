from ..config import BASE_DIR
import yaml as __yaml


def load_yaml(path: str) -> dict:
    with open(BASE_DIR + path, 'r') as stream:
        return __yaml.safe_load(stream)


def get_jobs() -> dict:
    return load_yaml("/jobs/jobs.yaml")["jobs"]


def get_job(name: str) -> dict:
    return get_jobs()[name]


def get_secuences() -> dict:
    return load_yaml("/jobs/secuences.yaml")["secuences"]


def get_secuence(name: str) -> dict:
    return get_secuences()[name]
