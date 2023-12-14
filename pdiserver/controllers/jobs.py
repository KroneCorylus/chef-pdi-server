import json
from pdiserver import services
from flask import Blueprint, request

jobs_blueprint = Blueprint('jobs', __name__)


@jobs_blueprint.route("/")
def get_jobs():
    jobs = list(services.yaml.get_jobs())
    return json.dumps(jobs)


@jobs_blueprint.route("/<path:job>")
def define_job(job):
    return services.job.define_job(job)


@jobs_blueprint.route("/<path:job_name>/executions", methods=['GET'])
def get_executions(job_name):
    return json.dumps(services.job.get_executions(job_name))


@jobs_blueprint.route("/<path:job_name>/executions/<path:id>", methods=['GET'])
def get_execution_log(job_name, id):
    return services.job.get_execution(job_name, id)


@jobs_blueprint.route("/<path:job_name>/executions", methods=['POST'])
def execute_job(job_name):
    print(request.get_json(silent=True))
    argsDict = request.get_json(silent=True)
    return services.job.execute(job_name, argsDict)
