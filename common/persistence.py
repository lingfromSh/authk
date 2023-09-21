from datetime import datetime

from tortoise import Model
from tortoise import fields
from tortoise.manager import Manager
from tortoise.queryset import QuerySet

# alias of Manager
AllObjectManager = Manager


# Add soft delete method to QuerySet
class ActiveQuerySet(QuerySet):
    async def soft_delete(self):
        # TODO: autoset deleted_by as current operator
        await self.update(deleted_at=datetime.utcnow().timestamp(), deleted_by="Operator")


# Only output non-deleted objects
class ActiveObjectManager(Manager):
    def get_queryset(self) -> ActiveQuerySet:
        return ActiveQuerySet(self._model).filter(deleted_at=0, deleted_by__isnull=True)


class DeletedObjectManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().exclude(deleted_at=0, deleted_by__isnull=True)


class BaseModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True, description="created at")
    created_by = fields.ForeignKeyField("models.Endpoint", description="created by")
    modified_at = fields.DatetimeField(auto_now=True, description="modified at")
    modified_by = fields.ForeignKeyField("models.Endpoint", description="modified by")
    deleted_at = fields.BigIntField(default=0, description="deleted at(timestamp-ns)")
    deleted_by = fields.ForeignKeyField("models.Endpoint", null=True, description="deleted by")

    # purpose for filtering deleted objects
    deleted_objects = DeletedObjectManager()

    async def soft_delete(self, using_db=None):
        self.deleted_at = datetime.utcnow().timestamp()
        # TODO: autoset deleted_by as current operator
        self.deleted_by = "Operator ID"
        await self.save(using_db=using_db, update_fields=["deleted_at", "deleted_by"])

    class Meta:
        abstract = True
        manager = ActiveObjectManager
