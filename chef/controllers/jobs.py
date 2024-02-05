import json

from security.auth_jtw import token_required

from helpers.flask_error_handler import flask_error_handler
import services
from flask import Blueprint, request
from config import ROLE

jobs_blueprint = Blueprint('jobs', __name__)


@jobs_blueprint.route("/")
@token_required(ROLE)
def get_jobs():
    try:
        return services.yaml.get_jobs().toDict()
    except Exception as err:
        return flask_error_handler(500, str(err))


@jobs_blueprint.route("/<path:job_name>")
@token_required(ROLE)
def define_job(job_name):
    return services.job.define_job(job_name).toJson()


@jobs_blueprint.route("/<path:job_name>/executions", methods=['GET'])
@token_required(ROLE)
def get_executions(job_name):
    return json.dumps(services.job.get_executions(job_name))


@jobs_blueprint.route("/<path:job_name>/executions/<path:id>", methods=['GET'])
@token_required(ROLE)
def get_execution_log(job_name, id):
    return services.job.get_execution(job_name, id) or ''


@jobs_blueprint.route("/<path:job_name>/executions", methods=['POST'])
@token_required(ROLE)
def execute_job(job_name):
    print(request.get_json(silent=True))
    job_parameter_overwrites = request.get_json(silent=True) or {}
    return services.job.execute(job_name, job_parameter_overwrites)
