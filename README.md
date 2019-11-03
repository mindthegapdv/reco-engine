# reco-engine


## Initial loading of Neo4j GraphDB

`python3 load_data.py`  to run all the data manipulations and table joins

### Update datasets in static files 
`git add -A`

`git commit -m 'updated datasets'`

`git push heroku master`

### Load data into graphdb
`python3 provision.py`


## Endpoints 101
But how do we update and get data from our lovely graphdb??? 

### Create order
@app.route('/create-order/<order_num>/<date>/<time>')
Example: `http://need2feed-ai.herokuapp.com/add-participant/18/Uzair.Emerson@need2feed.us`

### Add cuisine to order
@app.route('/add-cuisine/<order_num>/<cuisine>')
Example: `http://need2feed-ai.herokuapp.com/add-cuisine/18/Italian`

### Add participant to order
@app.route('/add-participant/<order_num>/<email>')
Example: `http://need2feed-ai.herokuapp.com/add-participant/18/Uzair.Emerson@need2feed.us`

### Add participant likes order relationship
@app.route('/like/<order_num>/<email>')
Example: `http://need2feed-ai.herokuapp.com/like/18/Uzair.Emerson@need2feed.us`

### Add participant likes order relationship
@app.route('/dislike/<order_num>/<email>')
Example: `http://need2feed-ai.herokuapp.com/dislike/18/Uzair.Emerson@need2feed.us`

### Get multiplier in % that the coordinator should increase or decrease the order by for less food waste
@app.route('/fit/<order_num>')
Example: `http://need2feed-ai.herokuapp.com/fit/18`

