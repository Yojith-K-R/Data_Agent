from fastapi import FastAPI

from data_agent.api.routes import router
from data_agent.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(router)