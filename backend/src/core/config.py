from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')
    
    DATABASE_URL: str = "sqlite:///./expenses.db"
    OPENAI_API_KEY: str
    FIREBASE_ADMIN_SDK_PATH: str

settings = Settings()