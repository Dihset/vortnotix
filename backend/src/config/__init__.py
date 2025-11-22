from src.config.database import PostgresSettings
from src.config.general import GeneralSettings


class Settings(
    PostgresSettings,
    GeneralSettings,
):
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
