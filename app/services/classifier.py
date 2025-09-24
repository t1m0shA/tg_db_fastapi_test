from app.config.settings import settings
from openai import OpenAI
from app.services.base import BaseClassifier


class MockClassifier(BaseClassifier):

    def __init__(self):

        self.TEXT_KEYWORDS, self.BIO_KEYWORDS = settings.load_keywords()

    def classify(self, text: str, bio: str) -> bool:

        text_lower = text.lower()
        bio_lower = bio.lower()

        text_match = any(word in text_lower for word in self.TEXT_KEYWORDS)
        bio_match = any(word in bio_lower for word in self.BIO_KEYWORDS)

        return text_match or bio_match


class OpenAIClassifier(BaseClassifier):

    def __init__(self, api_key: str):

        self.client = OpenAI(api_key=api_key)

    def classify(self, text: str, bio: str) -> bool:

        openai_prompts = settings.load_prompts()

        try:
            prompt = openai_prompts["prompt"]
        except KeyError:
            raise

        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": settings.openai_role,
                    "content": prompt,
                },
                {"text": text, "bio": bio},
            ],
            max_tokens=5,
        )
        content = response.choices[0].message.content.lower()
        return "lead" in content


class ClassifierFactory:
    """Factory to create classifier service based on config."""

    @staticmethod
    def create() -> BaseClassifier:
        if USE_OPENAI and OPENAI_API_KEY:
            return OpenAIClassifier(api_key=OPENAI_API_KEY)
        return MockClassifier()
