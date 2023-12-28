import json

from ..security.auth_jtw import token_required

from ..helpers.flask_error_handler import flask_error_handler
from .. import services
from flask import Blueprint, request

jobs_blueprint = Blueprint('jobs', __name__)


@jobs_blueprint.route("/")
@token_required()
def get_jobs():
    try:
        jobs = list(services.yaml.get_jobs())
        return json.dumps(jobs)
    except Exception as err:
        return flask_error_handler(500, str(err))


@jobs_blueprint.route("/<path:job>")
@token_required()
def define_job(job):
    return services.job.define_job(job)


@jobs_blueprint.route("/<path:job_name>/executions", methods=['GET'])
@token_required()
def get_executions(job_name):
    return json.dumps(services.job.get_executions(job_name))


@jobs_blueprint.route("/<path:job_name>/executions/<path:id>", methods=['GET'])
@token_required()
def get_execution_log(job_name, id):
    return services.job.get_execution(job_name, id)


@jobs_blueprint.route("/<path:job_name>/executions", methods=['POST'])
@token_required()
def execute_job(job_name):
    print(request.get_json(silent=True))
    argsDict = request.get_json(silent=True)
    return services.job.execute(job_name, argsDict)
