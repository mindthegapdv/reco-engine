# this is less of a test and more to just see what all the fit scores are for all historical orders... 
import requests

# lists all "preference" scores for existing orders 

def find_fit(order):
	r = str("https://need2feed-ai.herokuapp.com/fit/%s" % order)
	n = requests.get(r).content
	return n


for order in range(85):
	order = order+1
	r = find_fit(order).decode("utf-8")
	print([order,r])
