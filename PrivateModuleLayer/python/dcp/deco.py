import json
from botocore.client import ClientError

def lambda_handle_exception(logger):
    def _lambda_handle_exception(func):
        def handle_exception_wrapper(*args, **kwargs):
 
            try:
                print(json.dumps(args[0]))
                return func(*args, **kwargs)
            except ClientError as e:
                logger.error(e, stack_info=True)
                raise e
            except Exception as e:
                logger.error(e, stack_info=True)
                raise e

        return handle_exception_wrapper
 
    return _lambda_handle_exception

