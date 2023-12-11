from pdiserver.controllers.jobs import jobs_blueprint
from pdiserver.controllers.secuences import secuences_blueprint
from flask import Flask


app = Flask(__name__)
app.register_blueprint(jobs_blueprint, url_prefix="/jobs")
app.register_blueprint(secuences_blueprint, url_prefix="/secuences")


@app.route("/")
def hello():
    return 'hello'
