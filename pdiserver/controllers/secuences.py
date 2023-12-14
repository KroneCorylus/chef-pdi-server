import json
from flask import Blueprint
from pdiserver import services
secuences_blueprint = Blueprint('secuences', __name__)


@secuences_blueprint.route("/")
def get_secuences():
    secuences = list(services.yaml.get_secuences())
    return json.dumps(secuences)


@secuences_blueprint.route("/<path:secuence>")
def define_secuence(secuence):
    return json.dumps(services.yaml.get_secuence(secuence))


@secuences_blueprint.route("/<path:secuence_name>/executions", methods=['POST'])
def execute_secuence(secuence_name):
    return services.secuence.execute(secuence_name)
