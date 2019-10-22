#!/bin/bash

while getopts m OPT
do
  case $OPT in
    "m" ) FLG_INSTALL_MODULE="TRUE" ;;
      * ) echo "Usage: [-m]"
          echo "m: install modules to PublicModuleLayer"
          exit 1 ;;
  esac
done

if [ "$FLG_INSTALL_MODULE" = "TRUE" ]; then
  rm -rf ./PublicModuleLayer/python
  mkdir ./PublicModuleLayer/python
  pip install -r ./PublicModuleLayer/requirements.txt -t ./PublicModuleLayer/python
fi

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

