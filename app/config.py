from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    anthropic_api_key: str
    model: str = "claude-haiku-4-5-20251001"
    max_tokens: int = 1024
    port: int = 8000
    host: str = "127.0.0.1"
    test: str = "This is a test variable"


settings = Settings(test="This is a test variable from settings declaration")