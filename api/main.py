from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.conf.settings import Settings
from api.routers.currency_router import currency_router

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME.format(name="API Service"),
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_STR}/openapi.json",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(currency_router)
