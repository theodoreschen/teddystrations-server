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

## Running
```
docker-compose up -d
python3 main.py
```
