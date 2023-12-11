from pdiserver.config import BASE_DIR
import yaml


def get_jobs() -> dict:
    with open(BASE_DIR + "/jobs/jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded["jobs"]
