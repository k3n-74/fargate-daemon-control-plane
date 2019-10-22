import os

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from datetime import datetime

class DaemonMasterModel(Model):
    class Meta:
        table_name = os.environ['EnvName'] + '-daemon-master'
        region = 'ap-northeast-1'

    # attributes
    daemon_id = UnicodeAttribute(attr_name='daemon-id', null=False, hash_key=True)
    daemon_status_desired = UnicodeAttribute(attr_name='daemon-status-desired', null=True)
    daemon_status_last = UnicodeAttribute(attr_name='daemon-status-last', null=True)
    daemon_status_changed_at = UTCDateTimeAttribute(attr_name='daemon-status-changed-at', null=True)

    replace_job_id = UnicodeAttribute(attr_name='replace-job-id', null=True)
    replace_status_desired = UnicodeAttribute(attr_name='replace-status-desired', null=True)
    replace_status_last = UnicodeAttribute(attr_name='replace-status-last', null=True)
    replace_status_changed_at = UTCDateTimeAttribute(attr_name='replace-status-changed-at', null=True)

    task_current_arn = UnicodeAttribute(attr_name='task-current-arn', null=True)
    task_current_private_ip = UnicodeAttribute(attr_name='task-current-private-ip', null=True)
    task_current_status_desired = UnicodeAttribute(attr_name='task-current-status-desired', null=True)
    task_current_status_last = UnicodeAttribute(attr_name='task-current-status-last', null=True)
    task_current_status_changed_at = UTCDateTimeAttribute(attr_name='task-current-status-changed-at', null=True)

    task_next_arn = UnicodeAttribute(attr_name='task-next-arn', null=True)
    task_next_privte_ip = UnicodeAttribute(attr_name='task-next-privte-ip', null=True)
    task_next_status_desired = UnicodeAttribute(attr_name='task-next-status-desired', null=True)
    task_next_status_last = UnicodeAttribute(attr_name='task-next-status-last', null=True)
    task_next_status_changed_at = UTCDateTimeAttribute(attr_name='task-next-status-changed-at', null=True)

    task_drain_arn = UnicodeAttribute(attr_name='task-drain-arn', null=True)
    task_drain_private_ip = UnicodeAttribute(attr_name='task-drain-private-ip', null=True)
    task_drain_status_desired = UnicodeAttribute(attr_name='task-drain-status-desired', null=True)
    task_drain_status_last = UnicodeAttribute(attr_name='task-drain-status-last', null=True)
    task_drain_status_changed_at = UTCDateTimeAttribute(attr_name='task-drain-status-changed-at', null=True)

# https://github.com/pynamodb/PynamoDB/issues/198

