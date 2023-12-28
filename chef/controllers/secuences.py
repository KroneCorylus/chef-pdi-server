from ..security.auth_jtw import token_required
import json
from flask import Blueprint
from .. import services
secuences_blueprint = Blueprint('secuences', __name__)


@secuences_blueprint.route("/")
@token_required()
def get_secuences():
    secuences = list(services.yaml.get_secuences())
    return json.dumps(secuences)


@secuences_blueprint.route("/<path:secuence_name>")
@token_required()
def define_secuence(secuence_name):
    return json.dumps(services.yaml.get_secuence(secuence_name))


@secuences_blueprint.route("/<path:secuence_name>/executions", methods=['POST'])
@token_required()
def execute_secuence(secuence_name):
    return services.secuence.execute(secuence_name)


@secuences_blueprint.route("/<path:secuence_name>/executions")
@token_required()
def get_executions(secuence_name):
    return json.dumps(services.secuence.get_executions(secuence_name))


@secuences_blueprint.route("/<path:secuence_name>/executions/<path:id_execution>")
@token_required()
def get_job_executions(secuence_name: str, id_execution: int):
    return json.dumps(services.job.get_executions_by_secuence_id(id_execution))
