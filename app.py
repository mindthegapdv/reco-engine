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

@app.route("/test1")

def hello():
	query = "MATCH (participant:Participant) RETURN participant limit 3"
	result = graph.run(query)

	return str([get_email(record['participant']) for record in result])


# create order 
# date = yyyy-mm-dd
# time = hh:ss
@app.route('/create/<date>/<time>')

def create_order(order_num,date,time):
	query = '''CREATE (o:Order) 
			SET o.date = %s, o.time = %s''' % (date, time)
	graph.run(query)

	return "Order created for " + str(date) + " at " + str(time)

# link order and participant 
@app.route('/fit/<order>/<participant>')

def find_fit(order):
	query = '''MATCH (c1:Cuisine)-[r1]-(o:Order)-[r2:PARTICIPATED_IN]-(p:Participant)-[r3:LIKES]-(c2)
			WHERE id(o) = %s
			AND c1=c2
			RETURN p.email as email, r3.value as affinity, p.weight as weight''' %order
	df = pd.DataFrame(graph.run(query))
	df.columns=['email', 'affinity', 'weight']


	query = '''MATCH (c1:Cuisine)-[r1]-(o:Order)-[r2:PARTICIPATED_IN]-(p:Participant)
			WHERE id(o) = %s
			RETURN count(p)''' % order

	return str(order) + " linked with " + str(participant)


@app.route('/fit/<order>')

def find_fit(order):
	query = '''MATCH (c1:Cuisine)-[r1]-(o:Order)-[r2:PARTICIPATED_IN]-(p:Participant)-[r3:LIKES]-(c2)
			WHERE id(o) = %s
			AND c1=c2
			RETURN p.email as email, r3.value as affinity, p.weight as weight''' %order
	df = pd.DataFrame(graph.run(query))
	df.columns=['email', 'affinity', 'weight']


	query = '''MATCH (c1:Cuisine)-[r1]-(o:Order)-[r2:PARTICIPATED_IN]-(p:Participant)
			WHERE id(o) = %s
			RETURN count(p)''' % order

	return str([get_email(record['participant']) for record in result])


@app.route("/test2")
def test():
    return "meow"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)