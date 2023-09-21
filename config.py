TORTOISE_ORM = {
    "connections": {"default": "sqlite://sqlite.db"},
    "apps": {
        "models": {
            "models": ["models.endpoint", "models.entity", "models.operation", "aerich.models"],
            "default_connection": "default",
        },
    },
}
