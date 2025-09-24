from app.errors import ClassifierNotConfiguredError


class BaseClassifier:

    async def classify(self, text: str, bio: str) -> bool:

        raise ClassifierNotConfiguredError()
