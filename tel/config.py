from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class TelegramSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    telegram_api_id: int
    telegram_api_hash: str
    telegram_phone: str
    telegram_session: str
    telegram_chat: str

    classification_resource: str


settings = TelegramSettings()
