[![Build Status](https://tchen25.visualstudio.com/Teddystrations/_apis/build/status/theodoreschen.teddystrations-server?branchName=master)](https://tchen25.visualstudio.com/Teddystrations/_build/latest?definitionId=10&branchName=master) ![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/tchen25/Teddystrations/10) ![Azure DevOps tests](https://img.shields.io/azure-devops/tests/tchen25/Teddystrations/10)

# teddystrations-server
Backend server running teddystrations game

## Requirements
- Python3.6+
- Docker

## Installation
Highly recommended this is done in a virtualenv because you should anyway.

```
pip3 install -r requirements.txt
```

## Building Docker Image
Included in the files is a build script `docker_build.sh`. The Python modules
found in the `requirements.txt` need to be installed.

## Running

```
docker-compose up -d
uwsgi --ini game-server.ini
```

### ADMIN_UUID
There is a setting in the `docker-compose.yml` that provides the option to
set your own custom ADMIN_UUID. If it's unset, then by default the game will
use the ADMIN_UUID of `01234567-0123-4567-89ab-0123456789ab`. This functions
as a secret token so only the person that is running the game has access to
game navigation options.
