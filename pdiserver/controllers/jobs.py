import json
import yaml
from pdiserver.services.pdiservice import getCommand, executeCommand
from pdiserver.config import BASE_DIR
from flask import Blueprint, request
jobs_handlers = Blueprint('dbscan_handlers', __name__)


@jobs_handlers.route("/")
def get_jobs():
    with open(BASE_DIR + "/jobs/jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    jobs = list(data_loaded["jobs"])
    print(jobs)
    return json.dumps(jobs)


@jobs_handlers.route("/<path:job>")
def define_job(job):
    with open(BASE_DIR + "/jobs/jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    result = data_loaded["jobs"][job]
    return result


@jobs_handlers.route("/<path:job>/execute")
def execute_job(job):
    argsDict = request.args.to_dict()
    with open(BASE_DIR + "/jobs/jobs.yaml", 'r') as stream:
        jobsconfig = yaml.safe_load(stream)
    jobParameters = jobsconfig["jobs"][job]["default_parameters"]
    jobParameters.update(argsDict)
    jobPath = jobsconfig["jobs"][job]["path"]
    command = getCommand(jobPath, jobParameters)
    return executeCommand(command)
