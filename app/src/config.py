from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / '.env'),
        env_prefix='',  
        extra='ignore'
    )

    
class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS: str
    OPENAI_API_KEY: str
    db: DatabaseSettings = DatabaseSettings()

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / '.env'),
        env_prefix='',
        extra='ignore' 
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseSettings()
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
