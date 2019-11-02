# app.py

import os

from py2neo import Graph, Node, Relationship
import pandas as pd

from flask import Flask, request, jsonify
app = Flask(__name__)

graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)


def get_email(participant):
    return {
        'id': participant['id'],
        'email': participant['email'],
    }

@app.route("/")

def hello():
	query = "MATCH (participant:Participant) RETURN participant limit 3"
	result = graph.run(query)

	return str([get_email(record['participant']) for record in result])



@app.route("/test")
def test():
    return "meow"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)