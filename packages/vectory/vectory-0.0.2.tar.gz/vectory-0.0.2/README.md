# Pento Open Source Software

To use OSS you will need [pyenv](https://github.com/pyenv/pyenv-installer), [poetry](https://python-poetry.org/docs/#installation) and docker

Install steps:

`$ CONFIGURE_OPTS=--enable-loadable-sqlite-extensions pyenv install`

`$ python -m venv .venv`

`$ source .venv/bin/activate`

`$ poetry install`

`$ docker-compose up`

You can check the cli commands by running `oss --help`
