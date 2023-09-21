from tortoise import fields

from common.persistence import BaseModel


class Endpoint(BaseModel):
    entity = fields.ForeignKeyField(
        "models.Entity", related_name="used_by_endpoints", on_delete=fields.RESTRICT, description="model of endpoint"
    )
    external_id = fields.CharField(max_length=255, unique=True, description="external id for external usage", index=True)
    data = fields.JSONField(description="data of endpoint")
