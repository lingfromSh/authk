from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "endpoint" ADD "entity_id" INTEGER NOT NULL CONSTRAINT fk_endpoint_entity_c4eae64f REFERENCES entity/* model of endpoint */;
        """  # NOQA


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "endpoint" DROP FOREIGN KEY "fk_endpoint_entity_c4eae64f";
        ALTER TABLE "endpoint" DROP COLUMN "entity_id";"""
