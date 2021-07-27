# MFS Africa Backend Challenge

## Deploy using Docker
For quick setup, use docker.
### Requirements

* Docker
* Docker-compose

### Ports
* 80,443 - `Nginx Webserver`


### Setup

```shell
bash setup_docker.sh
```

## Run using django server
This method allows you to run django server in the case docker doesn't run.
### Requirements
* Ubuntu 16+
* Redis
* Python3.6+
* Postgres10+
## Install

Relé supports Python 3.6+ and installing via ``pip``

`pip install rele`

or with Django integration

`pip install rele[django]`

or with Flask integration

`pip install rele[flask]`


### Development

You can install [pre-commit](https://pre-commit.com/) hooks to apply formatting on your code before it gets committed or pushed.

**NOTE:** pre-commit hooks require python3 to be installed.

Install `pre-commit` and its hooks (only need once):

    pip install pre-commit
    # to run checks on every 'git commit ...' install hooks via:
    pre-commit install

    # alternatively, to run checks on 'git push ...' only, use:
    pre-commit install -t pre-push

Afterwards pre-commit will run whenever you `git commit ...` or `git push ...`.


#### Run pipeline in dev, staging & production environments:
Push changes to develop, staging and production branches respectively
