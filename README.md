# classification-api
A service that stores results from a classification service in a database and make them available through a REST API. It is meant to run on the edge, that is, a computing device that is deployed in a factory.


## Installation
* Install Docker
* Build docker image with `docker-compose build`

* Install postgresql on docker:
```
docker network create --driver bridge postgres-network
```

## Run the tests
```
docker-compose pytest
```

## Start locally
* Start web server `
  docker-compose run -e FLASK_APP=controllers.py -e FLASK_ENV=development -p 5000:5000 api
`
* Start message queue consumer `
  docker-compose run consumer
`

## API usage
# Tests
Publishing a new message in the queue:
```
mosquitto_pub -t new_prediction -m '{"algorithm": {"name": "DeevioNet","version": "1.0"},"status":"complete","imagePath":"20180907/1536311270718.jpg","imageId":"1536311270718","output":[{"bbox":[1008.8831787109375,280.6226501464844,1110.0245361328125,380.72021484375],"probability":0.9725130796432495,"label":"nail","result":"good"} ]}'
```
Get weak predictions
```
http://localhost:5000/v1/predictions/weak
```
Get last prediction for an imageId
```
http://localhost:5000/v1/predictions/1536311270718
```

More on [localhost:5000/](http://localhost:5000/)

## Deploy (to production)
Currently not implemented
