"""
OPA is expected to be running on default port 8181
"""

import json
import logging

from flask import Flask, request, abort

from flask_opa import OPA, OPAException


def parse_input():
    return {
        "input": {
            "method": request.method,
            "path": request.path.strip().split("/")[1:],
            "user": request.headers.get("Authorization", ""),
        }
    }


app = Flask(__name__)
opa = OPA(app, parse_input, url="http://localhost:8181/v1/data/examples/allow")
app.logger.setLevel(logging.DEBUG)
opa.init_app(app)

data = {
    'eliux': {
        "fullname": "Eliecer Hernandez",
        "country": "Cuba",
        "age": 32,
        "ssn": "000-12-77632",
        "biography": "Was born in 1985 into a humble family..."
    }
}


@app.route("/")
def welcome_page():
    return "Hello Flask-OPA user! Lets see some data. " \
           "Follow the instructions in the README of examples."


@app.route("/list", methods=['GET'])
def available_persons():
    return json.dumps(list(data.keys()))


@app.route("/data/<who>", methods=['GET'])
def show_data_of(who):
    if who in data:
        return json.dumps(data[who])
    else:
        return json.dumps({
            "message": "%s was not found in our system" % who
        }), 404


@app.route("/data/<who>", methods=['POST'])
def set_data_of(who):
    data[who] = json.loads(request.data)
    return json.dumps(data[who])


@app.route("/data/<who>", methods=['DELETE'])
def delete(who):
    if who not in data:
        return json.dumps({
            "message": "%s was not found in our system" % who
        }), 404
    del data[who]
    return json.dumps(None), 204


@app.errorhandler(OPAException)
def handle_opa_exception(e):
    return json.dumps({
        "message": str(e)
    }), 403


if __name__ == '__main__':
    app.run(debug=True)
