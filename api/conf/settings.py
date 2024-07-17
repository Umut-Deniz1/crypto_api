from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    ENV: str
    DEBUG: bool
    API_STR: str = "/api/v1"
    PROJECT_NAME: str = "{name}"
    PROJECT_VERSION: str = "v1"

    # POSTGRES
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PORT: int

    # Request Auth
    CLIENT_X_AUTH: str

    # origins
    STAGING_ORIGIN: list = ["http://localhost:8000"]
    PRODUCTION_ORIGIN: list = []

    @property
    def ORIGIN(self):
        if self.ENV == "PRODUCTION":
            return self.PRODUCTION_ORIGIN
        else:
            return self.STAGING_ORIGIN

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"
