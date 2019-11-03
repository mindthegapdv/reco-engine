import os
import statistics

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
    

@app.route("/test")

def test():
	query = "MATCH (p:Participant) RETURN count(p) as count"
	result = graph.run(query)

	return str([get_count(record['count']) for record in result][0])


# Endpoint: Create order 
# order_num needs to come from REST API, above 1000 pls
# date = yyyy-mm-dd
# time = hh:ss
@app.route('/create-order/<order_num>/<date>/<time>')

def create_order(order_num,date,time):
	query = '''CREATE (o:Order) 
			SET o.order_id = toInteger(%s), o.date = "%s", o.time = "%s"''' % (order_num, date, time)
	graph.run(query)

	return "Order number " + str(order_num) + " created for " + str(date) + " at " + str(time)


# Endpoint: Add cuisine to order
@app.route('/create-order/<order_num>/<cuisine>')

def create_order(order_num,cuisine):
	query = '''MATCH (c:Cuisine), (o:Order)
			WHERE o.order_id = %s and c.name = "%s"
			''' % (order_num, cuisine)
	graph.run(query)

	return str(cuisine) + "added to order number " + str(order_num)


# Endpoint: Add participant to order
@app.route('/add-participant/<order_num>/<email>')

def add_participant(order_num,email):
	query = '''MATCH (p:Participant), (o:Order)
			WHERE p.email = "%s" and o.order_id = %s
			MERGE (p)-[r:PARTICIPATED_IN]->(o)
			SET r.value = 0''' % (email, order_num)
	graph.run(query)

	return str(email) + " added to order number " + str(order_num)


# Endpoint: Add participant likes order relationship
@app.route('/like/<order_num>/<email>')

def like(order_num,email):
	query = '''MATCH (p:Participant)-[r:PARTICIPATED_IN]-(o:Order)-[r2:ORDERED]-(c:Cuisine)
			WHERE p.email = "%s" and o.order_id = %s 
			MERGE (p)-[r3:LIKES]->(c)
			WITH r3, r3.value as val
			SET r3.value = val + 1''' % (email, order_num) # adds one "like" point in the relationship 
	graph.run(query)

	return str(email) + " likes " + str(order_num)


# Endpoint: Add participant dislikes meal relationship
@app.route('/dislike/<order_num>/<email>/')

def dislike(order_num,email):
	query = '''MATCH (p:Participant)-[r:PARTICIPATED_IN]-(o:Order)-[r2:ORDERED]-(c:Cuisine)
			WHERE p.email = "%s" and o.order_id = %s
			MERGE (p)-[r3:LIKES]->(c)
			WITH r3, r3.value as val
			SET r3.value = val - 1''' % (email, order_num) # subtracts one "like" point in the relationship 
	graph.run(query)

	return str(email) + " dislikes " + str(order_num)


# gets multiplier in % that the coordinator should increase or decrease the order by for less food waste
@app.route('/fit/<order_num>')

def find_fit(order_num):
	# returns total affinity of participant to the food that is ordered 
	query = '''MATCH (c1:Cuisine)-[r1]-(o:Order)-[r2:PARTICIPATED_IN]-(p:Participant)-[r3:LIKES]-(c2)
			WHERE o.order_id = %s
			AND c1=c2
			RETURN p.email as email, r3.value as affinity, p.weight as weight''' % order_num
	df = pd.DataFrame(graph.run(query))
	df.columns = ['email', 'affinity', 'weight']

	sum_affinity = df.affinity.sum()
	query = '''MATCH (c1:Cuisine)-[r1]-(o:Order)-[r2:PARTICIPATED_IN]-(p:Participant)
			WHERE o.order_id = %s
			RETURN count(p) as count''' % order_num
	result = graph.run(query)
	participants = int([get_count(record['count']) for record in result][0])
	max_score = participants*5
	pref = sum_affinity/max_score

	# Mean weight of entire population in the dataset is 161 lbs. Anything over that = more food; anything under = less food
	# On average, 20 lbs = an increase of 12.6% increase in calories needed (according to some NHS paper)
	mean_weight = df.weight.mean()
	weight = (mean_weight - 161)/20*0.126

	# Assumptions:
	# 80-20 rule: you can ever only really please 80% of people, so anything above that = increase in food, below = decrease
	# cap max increase/decrease at 30% 
	fit = (pref-0.8)*0.3

	# return str([pref, weight])
	return str(statistics.mean([fit, weight]))



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)