# app.py

import os

from py2neo import Graph, Node, Relationship
import pandas as pd


graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)


def serialize_genre(participant):
    return {
        'id': participant['id'],
        'email': participant['email'],
    }


query = "MATCH (participant:Participant) RETURN participant limit 3"
result = graph.run(query)

print([serialize_genre(record['participant']) for record in result])


