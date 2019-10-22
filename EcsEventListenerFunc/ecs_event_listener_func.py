import json

from dcp.table_models import DaemonMasterModel
from datetime import datetime

from dcp.deco import lambda_handle_exception
from logging import getLogger
logger = getLogger()

@lambda_handle_exception(logger)
def lambda_handler(event, context):

    daemon_id = find_daemon_id_from_ecs_event(event)
    last_status = find_last_status_from_ecs_event(event)
    desired_status = find_desired_status_from_ecs_event(event)

    update_actions = []
    
    # start task:
    #   desired: RUNNING,      RUNNING, RUNNING
    #   last   : PROVISIONING, PENDING, RUNNING
    # stop task:
    #   desired: STOPPED, STOPPED,        STOPPED
    #   last   : RUNNING, DEPROVISIONING, STOPPED

    if desired_status == 'RUNNING' and last_status == 'PROVISIONING':
        set_last_status(update_actions, 'PROVISIONING')
        update_daemon_master(daemon_id, update_actions)
    elif desired_status == 'RUNNING' and last_status == 'PENDING':
        set_last_status(update_actions, 'PENDING')
        set_private_ip(update_actions, event)
        update_daemon_master(daemon_id, update_actions)
    elif desired_status == 'RUNNING' and last_status == 'RUNNING':
        set_last_status(update_actions, 'RUNNING')
        set_private_ip(update_actions, event)
        update_daemon_master(daemon_id, update_actions)
    elif desired_status == 'STOPPED' and last_status == 'RUNNING':
        pass
    elif desired_status == 'STOPPED' and last_status == 'DEPROVISIONING':
        set_last_status(update_actions, 'DEPROVISIONING')
        update_daemon_master(daemon_id, update_actions)
    elif desired_status == 'STOPPED' and last_status == 'STOPPED':
        set_last_status(update_actions, 'STOPPED')
        update_daemon_master(daemon_id, update_actions)
    else:
        pass

    return {
        'statusCode': 200
    }

def update_daemon_master(daemon_id, update_actions):
    daemon_item = DaemonMasterModel.get(daemon_id)
    daemon_item.update(actions=update_actions)

def set_last_status(update_actions, last_status):
    current_time = datetime.now()
    update_actions.append(DaemonMasterModel.daemon_status_last.set(last_status))
    update_actions.append(DaemonMasterModel.daemon_status_changed_at.set(current_time))
    update_actions.append(DaemonMasterModel.task_current_status_last.set(last_status))
    update_actions.append(DaemonMasterModel.task_current_status_changed_at.set(current_time))

def set_private_ip(update_actions, event):
    private_ip = find_private_ip_from_ecs_event(event)
    update_actions.append(DaemonMasterModel.task_current_private_ip.set(private_ip))

def find_daemon_id_from_ecs_event(event):
    container_overrides = event.get('detail').get('overrides').get('containerOverrides')
    for override in container_overrides:
        envs = override.get('environment')
        for env in envs:
            if env.get('name') == 'DCP_DAEMON_ID':
                daemon_id = env.get('value')
                print('daemon id: ' + daemon_id)
                return daemon_id
    raise Exception('Daemon ID is not found.')

def find_private_ip_from_ecs_event(event):
    attachments = event.get('detail').get('attachments')
    for attachment in attachments:
        details = attachment.get('details')
        for detail in details:
            if detail.get('name') == 'privateIPv4Address':
                return detail.get('value')
    raise Exception('Private IP is not found.')

def find_desired_status_from_ecs_event(event):
    desired_status = event.get('detail').get('desiredStatus')
    print('desired status: ' + desired_status)
    return desired_status

def find_last_status_from_ecs_event(event):
    last_status = event.get('detail').get('lastStatus')
    print('last status: ' + last_status)
    return last_status

