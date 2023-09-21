from tortoise import fields

from common.persistence import BaseModel


class Entity(BaseModel):
    name = fields.CharField(max_length=255, description="name of entity")
    desc = fields.CharField(max_length=255, description="description of entity")
    definition = fields.JSONField(source_field="def", description="definition of entity model")
    is_enabled = fields.BooleanField(default=False, description="is enabled")
    enabled_at = fields.DatetimeField(null=True, description="enabled at")
    enabled_by = fields.ForeignKeyField("models.Entity", description="enabled by")
