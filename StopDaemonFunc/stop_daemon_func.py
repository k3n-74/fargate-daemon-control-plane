import os
import json
import boto3
import time
from aws_xray_sdk.core import patch_all
from botocore.client import ClientError, Config
import traceback
from dcp.table_models import DaemonMasterModel

from datetime import datetime

from dcp.deco import lambda_handle_exception
from logging import getLogger
logger = getLogger()

patch_all()

@lambda_handle_exception(logger)
def lambda_handler(event, context):
    
    daemon_id = event.get('daemonId')
    cluster_arn = os.environ['ClusterArn']
    ecs = boto3.client('ecs')

    daemon_item = DaemonMasterModel.get(daemon_id)

    stop_daemon(ecs, daemon_item, cluster_arn)
    update_daemon_master(daemon_item)

    return {
        'statusCode': 200
    }

def stop_daemon(ecs, daemon_item, cluster_arn):
    stop_task_res = ecs.stop_task(
        cluster = cluster_arn,
        task = daemon_item.task_current_arn,
        reason = 'Stopped by Fargate Daemon Control Plane.'
    )

def update_daemon_master( daemon_item ):
    daemon_item.update(actions=[
        DaemonMasterModel.daemon_status_desired.set('STOPPED'),
        DaemonMasterModel.daemon_status_changed_at.set(datetime.now()),
        DaemonMasterModel.task_current_status_desired.set('STOPPED'),
        DaemonMasterModel.task_current_status_changed_at.set(datetime.now())
    ])

