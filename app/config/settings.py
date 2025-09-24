import json
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    openai_mock_keywords_text: list[str]
    openai_mock_keywords_bio: list[str]

    openai_role: str
    openai_model: str

    mock_keywords_file: Path = BASE_DIR / "data" / "mock_keywords.json"
    openai_prompts_file: Path = BASE_DIR / "data" / "openai_prompts.json"

    def load_keywords(self) -> tuple[list[str], list[str]]:

        with open(self.mock_keywords_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["text_keywords"], data["bio_keywords"]

    def load_prompts(self) -> dict[str, str]:

        with open(self.openai_prompts_file, "r", encoding="utf-8") as f:
            return json.load(f)


settings = Settings()
