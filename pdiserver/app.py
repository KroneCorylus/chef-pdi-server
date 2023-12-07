import subprocess
import yaml
from pdiserver.controllers.jobs import jobs_handlers
from flask import Flask


app = Flask(__name__)
app.register_blueprint(jobs_handlers, url_prefix="/jobs")


@app.route("/")
def hello():
    return 'hellos'


@app.route("/jobstest")
def jobstest():
    with open("/pdiserver/jobs/jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded


@app.route("/getparam")
def getparam():
    with open("/pdiserver/jobs/jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    params = ''
    for i in data_loaded["jobs"]["amis_trx_to_wh_pta"]["default_parameters"]:
        params = params + " -param:" + i
    return params


@app.route("/runtest")
def runtest():
    with open("/pdiserver/jobs/jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    params = ''
    for i in data_loaded["jobs"]["amis_trx_to_wh_pta"]["default_parameters"]:
        params = params + " -param:" + i
    runcommand = '/pdiserver/data-integration/kitchen.sh -file:' + '/pdiserver/jobs/' + \
        data_loaded["jobs"]["amis_trx_to_wh_pta"]["path"] + ' ' + params
    subprocess.run(runcommand, shell=True, executable="/bin/bash")
    return runcommand
