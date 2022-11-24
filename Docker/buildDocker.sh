#!/bin/bash

docker image build --platform linux/amd64 --no-cache -t admixpipe --file Dockerfile .
#docker buildx build --platform linux/amd64 --no-cache -t admixpipe --file Dockerfile .
#docker image build -t admixpipe --file Dockerfile .


exit

