#!/bin/bash

VERSION_TAG=0.0.2
python3 autobuild.py
source ~/venv/bin/activate
make clean
make html
docker rmi -f registry.aibee.cn/data_platform/dw-manual:$VERSION_TAG
docker build -t registry.aibee.cn/data_platform/dw-manual:$VERSION_TAG .
docker push registry.aibee.cn/data_platform/dw-manual:$VERSION_TAG
