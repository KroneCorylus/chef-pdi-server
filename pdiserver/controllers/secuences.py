import json
import yaml
from pdiserver.config import BASE_DIR
from flask import Blueprint

secuences_blueprint = Blueprint('secuences', __name__)


@secuences_blueprint.route("/")
def get_secuences():
    with open(BASE_DIR + "/jobs/secuences.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    secuences = list(data_loaded["secuences"])
    print(secuences)
    return json.dumps(secuences)


@secuences_blueprint.route("/<path:secuence>")
def define_secuence(secuence):
    with open(BASE_DIR + "/jobs/secuences.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded


@secuences_blueprint.route("/<path:secuence_name>/executions", methods=['POST'])
def execute_secuence(secuence_name):
    with open(BASE_DIR + "/jobs/secuences.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    secuence = data_loaded["secuences"][secuence_name]
    return secuence
