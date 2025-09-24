import httpx
from tel.config import settings


async def classify_message(text: str, bio: str) -> dict:

    async with httpx.AsyncClient() as http:

        resp = await http.post(
            settings.classification_resource, json={"text": text, "bio": bio}
        )
        resp.raise_for_status()

        return resp.json()
