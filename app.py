# app.py

import os
from neo4j.v1 import GraphDatabase, basic_auth

from py2neo import Graph, authenticate

import pandas as pd

from flask import Flask, request, jsonify
app = Flask(__name__)

graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)


@app.route("/")

def hello():
	query = "CREATE (n:Person { name: 'Matt', title: 'Right' })"
	graph.run(query)
	query = "MATCH n RETURN n.name as name, n.title as title"
	df = pd.DataFrame(graph.run(query))
	df.columns=['name', 'title']

	return df.head()


@app.route("/test")
def test():
    return "meow"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)