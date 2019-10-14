#!/bin/bash

mkdir ./CommonLayer/python
cp ./CommonLayer/dummy.py ./CommonLayer/python/dummy.py
pip install -r ./CommonLayer/requirements.txt -t ./CommonLayer/python

aws cloudformation package \
  --template-file daemon.yaml \
  --s3-bucket $CFN_S3_BUCKET \
  --s3-prefix $CFN_S3_PREFIX \
  --output-template-file daemon.yaml.packaged \
  --profile $AWS_CLI_PROFILE

aws cloudformation deploy \
  --stack-name daemon-daemon \
  --template-file daemon.yaml.packaged \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides EnvName=daemon \
  --profile $AWS_CLI_PROFILE

