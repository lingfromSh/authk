from typing import Tuple

from tortoise import Model
from tortoise import fields
from tortoise import timezone
from tortoise.manager import Manager
from tortoise.models import ModelMeta
from tortoise.queryset import QuerySet

# alias of Manager
AllObjectManager = Manager


# Add soft delete method to QuerySet
class ActiveQuerySet(QuerySet):
    async def soft_delete(self):
        # TODO: autoset deleted_by as current operator
        await self.update(deleted_at=timezone.now().timestamp(), deleted_by="Operator")


# Only output non-deleted objects
class ActiveObjectManager(Manager):
    def get_queryset(self) -> ActiveQuerySet:
        return ActiveQuerySet(self._model).filter(deleted_at=0, deleted_by__isnull=True)


class DeletedObjectManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().exclude(deleted_at=0, deleted_by__isnull=True)


class BaseModelMeta(ModelMeta):
    def __new__(mcs, name: str, bases: Tuple, attrs: dict):
        lower_name = name.lower()
        attrs["created_at"] = fields.DatetimeField(auto_now_add=True, description="created at")
        attrs["created_by"] = fields.ForeignKeyField(
            "models.Endpoint", related_name=f"created_{lower_name}", description="created by"
        )
        attrs["modified_at"] = fields.DatetimeField(auto_now=True, description="modified at")
        attrs["modified_by"] = fields.ForeignKeyField(
            "models.Endpoint", related_name=f"modified_{lower_name}", description="modified by"
        )
        attrs["deleted_at"] = fields.BigIntField(default=0, description="deleted at(timestamp-ns)")
        attrs["deleted_by"] = fields.ForeignKeyField(
            "models.Endpoint", null=True, related_name=f"deleted_{lower_name}", description="deleted by"
        )
        newcls = super().__new__(mcs, name, bases, attrs)
        return newcls


class BaseModel(Model, metaclass=BaseModelMeta):
    # purpose for filtering deleted objects
    deleted_objects = DeletedObjectManager()

    async def soft_delete(self, using_db=None):
        self.deleted_at = timezone.now().timestamp()
        # TODO: autoset deleted_by as current operator
        self.deleted_by = "Operator ID"
        await self.save(using_db=using_db, update_fields=["deleted_at", "deleted_by"])

    class Meta:
        abstract = True
        manager = ActiveObjectManager
