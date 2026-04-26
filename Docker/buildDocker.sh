#!/bin/bash

docker image build --platform linux/amd64 --no-cache -t admixpipe --file Dockerfile .

exit
