from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

class ToDoModel(Model):
    class Meta:
        table_name = 'todo_table'
        region = 'ap-northeast-1'
        write_capacity_units = 1
        read_capacity_units = 1

    # テーブル定義
    createdBy = UnicodeAttribute(hash_key=True, null=False)
    createdAt = UTCDateTimeAttribute(range_key=True, null=False, default=datetime.now())
    text = UnicodeAttribute(null=False)
    checked = BooleanAttribute(null=False, default=False)
    updatedAt = UTCDateTimeAttribute(null=False, default=datetime.now())

# https://github.com/pynamodb/PynamoDB/issues/198

