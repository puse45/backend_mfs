# MFS Africa Backend Challenge
Calculate the closest points, from comma separated values then store them in a table.

#### Expected details

* Store string of points submitted.
* Result of computation, The Closest pair.

## Deployment
Project can be deployed two ways.

1. Docker Container
2. Django Server(Development & test)

## Deploy using Docker
For quick setup, use docker.
### Requirements

* Docker
* Docker-compose

### Ports
Ensure below ports are not occupied by any running service.
* 80,443 - `Nginx Webserver`


### Setup

```shell
bash setup_docker.sh
```

### Admin
```shell
https://<host>/admin
email:admin@admin.com
password:admin
```

## Run using django server
This method allows you to run django server in case you would like.
### Requirements
* Ubuntu 16+
* Redis
* Python3.6+
* Postgres10+

### Run
Run develop server
```shell
# Migrate migrations
./manage.py migrate
# Run server
./manage.py runserver
```
### Test
```shell
./manage.py test pointer
```

### API Documentation

[Postman Collection](https://www.getpostman.com/collections/c557372d10e61f080bf7)
