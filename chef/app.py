from controllers.jobs import jobs_blueprint
from controllers.sequences import sequences_blueprint
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(jobs_blueprint, url_prefix="/jobs")
app.register_blueprint(sequences_blueprint, url_prefix="/sequences")


@app.route("/")
def itson():
    return 'Good news, Chef is working! v0.10.0'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=1882)
