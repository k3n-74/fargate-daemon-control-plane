import json

from dcp.deco import lambda_handle_exception
from logging import getLogger
logger = getLogger()

@lambda_handle_exception(logger)
def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
