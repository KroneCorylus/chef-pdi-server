from pdiserver.controllers.jobs import jobs_blueprint
from flask import Flask


app = Flask(__name__)
app.register_blueprint(jobs_blueprint, url_prefix="/jobs")


@app.route("/")
def hello():
    return 'hello'
