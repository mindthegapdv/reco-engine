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


def get_count(count):
    return count  
    

@app.route("/test1")

def hello():
	query = "MATCH (p:Participant) RETURN count(p) as count"
	result = graph.run(query)

	return str([get_count(record['count']) for record in result])


# create order 
# date = yyyy-mm-dd
# time = hh:ss
@app.route('/create-order/<order_num>/<date>/<time>')

def create_order(order_num,date,time):
	query = '''CREATE (o:Order) 
			SET o.order_id = toInteger(%s), o.date = "%s", o.time = "%s"''' % (order_num, date, time)
	graph.run(query)

	return "Order number " + str(order_num) + " created for " + str(date) + " at " + str(time)


# add participant to order
@app.route('/add-participant/<order_num>/<email>')

def add_participant(order_num,email):
	query = '''MATCH (p:Participant), (o:Order)
			WHERE p.email = "%s" and o.order_id = %s
			MERGE (p)-[r:PARTICIPATED_IN]->(o)
			SET r.value = 0''' % (email, order_num)
	graph.run(query)

	return str(email) + " added to order number " + str(order_num)


# add participant likes order
@app.route('/like/<order_num>/<email>')

def like(order_num,email):
	query = '''MATCH (p:Participant)-[r:PARTICIPATED_IN]-(o:Order)-[r2:ORDERED]-(c:Cuisine)
			WHERE p.email = "%s" and o.order_id = %s 
			MERGE (p)-[r3:LIKES]->(c)
			WITH r3, r3.value as val
			SET r3.value = val + 1''' % (email, order_num)
	graph.run(query)

	return str(email) + " likes " + str(order_num)


# add participant dislikes meal
@app.route('/dislike/<order_num>/<email>/')

def dislike(order_num,email):
	query = '''MATCH (p:Participant)-[r:PARTICIPATED_IN]-(o:Order)-[r2:ORDERED]-(c:Cuisine)
			WHERE p.email = "%s" and o.order_id = %s
			MERGE (p)-[r3:LIKES]->(c)
			WITH r3, r3.value as val
			SET r3.value = val - 1''' % (email, order_num)
	graph.run(query)

	return str(email) + " dislikes " + str(order_num)



@app.route('/fit/<order>')

def find_fit(order):
	query = '''MATCH (c1:Cuisine)-[r1]-(o:Order)-[r2:PARTICIPATED_IN]-(p:Participant)-[r3:LIKES]-(c2)
			WHERE o.order_id = %s
			AND c1=c2
			RETURN p.email as email, r3.value as affinity, p.weight as weight''' %order
	df = pd.DataFrame(graph.run(query))
	df.columns = ['email', 'affinity', 'weight']

	sum_affinity = df.affinity.sum()

	query = '''MATCH (c1:Cuisine)-[r1]-(o:Order)-[r2:PARTICIPATED_IN]-(p:Participant)
			WHERE o.order_id = %s
			RETURN count(p) as count''' % order
	result = graph.run(query)
	participants = int(result['count'])

	max_score = participants*5

	fit = sum_affinity/max_score

	return fit


@app.route("/test2")
def test():
    return "meow"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)