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


## Deploy (to production)
Currently not implemented