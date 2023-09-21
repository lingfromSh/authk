from fastapi import FastAPI

app = FastAPI(
    title="AuthK",
    description="A full-featured and out-of-box microservice which provides authn and authz.",
)


@app.on_event("startup")
async def startup_event():
    from helpers.setup import setup_tortoise_orm

    await setup_tortoise_orm(app)
