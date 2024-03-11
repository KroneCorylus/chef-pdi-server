from security.auth_jtw import token_required
import json
from flask import Blueprint
import services
from config import ROLE
sequences_blueprint = Blueprint('sequences', __name__)


@sequences_blueprint.route("/")
@token_required(ROLE)
def get_sequences():
    sequences = list(services.yaml.get_sequences().sequences)
    return json.dumps(sequences)


@sequences_blueprint.route("/<path:sequence_name>")
@token_required(ROLE)
def define_sequence(sequence_name):
    try:
        return json.dumps(
            services.yaml.get_seq(sequence_name).toDict()
        )
    except Exception as e:
        return str(e), 404


@sequences_blueprint.route("/<path:sequence_name>/executions", methods=['POST'])
@token_required(ROLE)
def execute_sequence(sequence_name):
    try:
        return services.sequence.execute(sequence_name)
    except Exception as e:
        return str(e), 404


@sequences_blueprint.route("/<path:sequence_name>/executions")
@token_required(ROLE)
def get_executions(sequence_name):
    return json.dumps(services.sequence.get_executions(sequence_name))


@sequences_blueprint.route("/<path:sequence_name>/executions/<path:id_execution>")
@token_required(ROLE)
def get_job_executions(sequence_name: str, id_execution: int):
    return json.dumps(services.job.get_executions_by_sequence_id(id_execution))
