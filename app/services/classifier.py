from app.config.settings import settings
from app.services.base import BaseClassifier
from app.errors import (
    ClassifierConnectionError,
    ClassificationFailedError,
    ClassifierNotConfiguredError,
)
from openai import AsyncOpenAI, APIConnectionError, RateLimitError
from asyncio import sleep


class MockClassifierService(BaseClassifier):

    async def classify(self, text: str, bio: str) -> bool:

        text_lower = text.lower()
        bio_lower = bio.lower()

        await sleep(2.5)

        text_match = any(
            word in text_lower for word in settings.openai_mock_keywords_text
        )
        bio_match = any(word in bio_lower for word in settings.openai_mock_keywords_bio)

        return text_match or bio_match


class OpenAIClassifierService(BaseClassifier):

    def __init__(self, api_key: str):

        self.client = AsyncOpenAI(api_key=api_key)

    async def classify(self, text: str, bio: str) -> bool:

        text_lower = text.lower()
        bio_lower = bio.lower()

        try:

            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": settings.openai_role,
                        "content": settings.openai_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"Text: {text_lower}\nBio: {bio_lower}",
                    },
                ],
                max_tokens=5,
            )
            content = response.choices[0].message.content.lower()
            return content.strip() == "lead"

        except (APIConnectionError, TimeoutError):
            raise ClassifierConnectionError()

        except RateLimitError:
            raise ClassificationFailedError(
                "The quota is reached for the OpenAI billing plan."
            )

        except Exception as exc:
            raise ClassificationFailedError(text=str(exc))


class ClassifierFactory:

    @staticmethod
    def create() -> BaseClassifier:

        if settings.use_mocked_openapi:
            return MockClassifierService()

        if not settings.openai_api_key:
            raise ClassifierNotConfiguredError(
                text="Missing API key for the classifier."
            )

        return OpenAIClassifierService(api_key=settings.openai_api_key)
