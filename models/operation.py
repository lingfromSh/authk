from tortoise import fields

from common.persistence import BaseModel


class DatabaseOperation(BaseModel):
    table = fields.CharField(max_length=255, description="operating table name")
    object_id = fields.BigIntField(source_field="oid", description="operating object id")
    attribute = fields.CharField(source_field="attr", max_length=255, description="attribute name in table")
    old_state = fields.CharField(source_field="ostate", max_length=255, description="prev state")
    current_state = fields.CharField(source_field="cstate", max_length=255, description="current state")

    class Meta:
        indexes = ("table", "object_id", "attribute")
