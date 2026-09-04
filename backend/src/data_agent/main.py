from fastapi import FastAPI

from data_agent.api.routes import router


app = FastAPI(
    title="Data Agent API",
    version="0.1.0",
)

app.include_router(router)