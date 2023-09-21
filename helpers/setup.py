from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise.contrib.fastapi import register_tortoise

if TYPE_CHECKING:
    from fastapi import FastAPI

TORTOISE_ORM = {
    "connections": {"default": "sqlite://sqlite.db"},
    "apps": {
        "models": {
            "models": ["models.endpoint", "models.entity", "models.operation", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def setup_tortoise_orm(application: FastAPI):
    """Setup tortoise orm before service starting receiving."""
    config = TORTOISE_ORM
    register_tortoise(application, config=config)
