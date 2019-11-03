# reco-engine


## Initial loading of Neo4j GraphDB

`python3 load_data.py`  to run all the data manipulations and table joins

### Update datasets in static files 
`git add -A`

`git commit -m 'updated datasets'`

`git push heroku master`

### Load data into graphdb
`python3 graphdb_provision.py`
Also resets database to factory condition if you mess up :) s


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

This request returns the affinity of each participant in relation to the cuisine that is being ordered. 

Then, the sum of "like" points is divided by the total potential # of "like" points given the size of the participant pool.

This is the initial fit of the cuisine in relation to the participants' preferences. 

Each particiipant is likely to have multiple cuisines that they "like".

Assumptions:
Mean weight of entire population in the dataset is 161 lbs. Anything over that = more food; anything under = less food
On average, 20 lbs = an increase of 12.6% increase in calories needed (according to some NHS paper)

80-20 rule: you can ever only really please 80% of people, so anything above that = increase in food, below = decrease
Cap max increase/decrease multiplier at 30% 

Take an average of these two multipliers for the final one.
