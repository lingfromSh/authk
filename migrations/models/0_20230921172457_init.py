from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "endpoint" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* created at */,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* modified at */,
    "deleted_at" BIGINT NOT NULL  DEFAULT 0 /* deleted at(timestamp-ns) */,
    "external_id" VARCHAR(255) NOT NULL UNIQUE /* external id for external usage */,
    "data" JSON NOT NULL  /* data of endpoint */,
    "created_by_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE /* created by */,
    "deleted_by_id" INT REFERENCES "endpoint" ("id") ON DELETE CASCADE /* deleted by */,
    "modified_by_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE /* modified by */
);
CREATE INDEX IF NOT EXISTS "idx_endpoint_externa_4938ce" ON "endpoint" ("external_id");
CREATE TABLE IF NOT EXISTS "entity" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* created at */,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* modified at */,
    "deleted_at" BIGINT NOT NULL  DEFAULT 0 /* deleted at(timestamp-ns) */,
    "name" VARCHAR(255) NOT NULL  /* name of entity */,
    "desc" VARCHAR(255) NOT NULL  /* description of entity */,
    "external_id" VARCHAR(255) NOT NULL UNIQUE /* external id for external usage */,
    "def" JSON NOT NULL  /* definition of entity model */,
    "is_enabled" INT NOT NULL  DEFAULT 0 /* is enabled */,
    "enabled_at" TIMESTAMP   /* enabled at */,
    "created_by_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE /* created by */,
    "deleted_by_id" INT REFERENCES "endpoint" ("id") ON DELETE CASCADE /* deleted by */,
    "enabled_by_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE /* enabled by */,
    "modified_by_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE /* modified by */
);
CREATE INDEX IF NOT EXISTS "idx_entity_externa_a25386" ON "entity" ("external_id");
CREATE TABLE IF NOT EXISTS "databaseoperation" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* created at */,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* modified at */,
    "deleted_at" BIGINT NOT NULL  DEFAULT 0 /* deleted at(timestamp-ns) */,
    "table" VARCHAR(255) NOT NULL  /* operating table name */,
    "oid" BIGINT NOT NULL  /* operating object id */,
    "attr" VARCHAR(255) NOT NULL  /* attribute name in table */,
    "ostate" VARCHAR(255) NOT NULL  /* prev state */,
    "cstate" VARCHAR(255) NOT NULL  /* current state */,
    "created_by_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE /* created by */,
    "deleted_by_id" INT REFERENCES "endpoint" ("id") ON DELETE CASCADE /* deleted by */,
    "modified_by_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE /* modified by */
);
CREATE INDEX IF NOT EXISTS "idx_databaseope_table_fbb9c0" ON "databaseoperation" ("table", "oid", "attr");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
