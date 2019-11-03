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
Request: `/add-participant/<order_num>/<email>`
Example: `http://need2feed-ai.herokuapp.com/add-participant/18/Uzair.Emerson@need2feed.us`

### Add cuisine to order
Request: `/add-cuisine/<order_num>/<cuisine>`
Example: `http://need2feed-ai.herokuapp.com/add-participant/18/Italian`

### Add participant to order
Request: `/add-participant/<order_num>/<email>`
Example: `http://need2feed-ai.herokuapp.com/add-participant/18/Uzair.Emerson@need2feed.us`

### 