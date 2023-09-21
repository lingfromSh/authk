from tortoise import fields

from common.persistence import BaseModel


class Entity(BaseModel):
    name = fields.CharField(max_length=255, description="name of entity")
    desc = fields.CharField(max_length=255, description="description of entity")
    external_id = fields.CharField(max_length=255, unique=True, description="external id for external usage", index=True)
    definition = fields.JSONField(source_field="def", description="definition of entity model")
    is_enabled = fields.BooleanField(default=False, description="is enabled")
    enabled_at = fields.DatetimeField(null=True, description="enabled at")
    enabled_by = fields.ForeignKeyField("models.Endpoint", related_name="enable_entities", description="enabled by")
