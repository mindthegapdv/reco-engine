import requests

# lists all "fit" scores for existing orders 
#spoiler alert: max = 0.975	min = 0.058823529

def get_data(order):
	r = str("https://need2feed-ai.herokuapp.com/fit/%s" % order)
	n = requests.get(r).content
	return n


for order in range(85):
	order = order+1
	r = get_data(order).decode("utf-8")
	print(r)

