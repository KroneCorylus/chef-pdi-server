import json
import yaml
from pdiserver.services.pdiservice import getCommand, executeCommand, get_job_executions, get_job_execution_log
from pdiserver.config import BASE_DIR
from flask import Blueprint, request

jobs_blueprint = Blueprint('dbscan_handlers', __name__)


@jobs_blueprint.route("/")
def get_jobs():
    with open(BASE_DIR + "/jobs/jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    jobs = list(data_loaded["jobs"])
    print(jobs)
    return json.dumps(jobs)


@jobs_blueprint.route("/<path:job>")
def define_job(job):
    with open(BASE_DIR + "/jobs/jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    result = data_loaded["jobs"][job]
    return result


@jobs_blueprint.route("/<path:job_name>/executions", methods=['GET'])
def get_executions(job_name):
    return json.dumps(get_job_executions(job_name))


@jobs_blueprint.route("/<path:job_name>/executions/logs/<path:id>", methods=['GET'])
def get_execution_log(job_name, id):
    return get_job_execution_log(job_name, id)


@jobs_blueprint.route("/<path:job_name>/executions", methods=['POST'])
def execute_job(job_name):
    print(request.get_json(silent=True))
    argsDict = request.get_json(silent=True)
    with open(BASE_DIR + "/jobs/jobs.yaml", 'r') as stream:
        jobsconfig = yaml.safe_load(stream)
    job = jobsconfig["jobs"][job_name]
    jobParameters = job["default_parameters"]
    jobParameters.update(argsDict)
    command = getCommand(job, jobParameters)
    return executeCommand(job_name, command)
