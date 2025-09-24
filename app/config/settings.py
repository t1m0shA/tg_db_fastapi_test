import json
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    openai_api_key: str
    openai_role: str
    openai_model: str
    openai_prompt: str | None = None

    use_mocked_openapi: bool
    openai_mock_keywords_text: list[str] = []
    openai_mock_keywords_bio: list[str] = []

    mock_keywords_file: Path = BASE_DIR / "data" / "mock_keywords.json"
    openai_prompts_file: Path = BASE_DIR / "data" / "openai_prompts.json"

    @model_validator(mode="after")
    def load_configs(self):

        with open(self.mock_keywords_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.openai_mock_keywords_text = data["text_keywords"]
            self.openai_mock_keywords_bio = data["bio_keywords"]

        with open(self.openai_prompts_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.openai_prompt = data["prompt"]

        return self


settings = Settings()
