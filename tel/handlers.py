from telethon import events, TelegramClient
from tel.config import settings
from telethon.tl.functions.users import GetFullUserRequest
from tel.classification import classify_message
from datetime import datetime
import httpx

client = TelegramClient(
    settings.telegram_session, settings.telegram_api_id, settings.telegram_api_hash
)
seen = set()


@client.on(events.NewMessage(chats=settings.telegram_chat, incoming=True))
async def handler(event):

    text = event.message.message
    if text in seen:
        return

    seen.add(text)

    sender = await event.get_sender()
    bio = None

    if sender:

        display_name = sender.first_name or ""
        if sender.last_name:
            display_name += f" {sender.last_name}"
        if sender.username:
            display_name += f" (@{sender.username})"

        try:
            full = await client(GetFullUserRequest(sender.id))
            bio = f"About user: {full.full_user.about}, Name: {display_name}"
        except Exception:
            bio = display_name

    print(
        f"{datetime.now()}. New unique message from @{settings.telegram_chat}: '{text}', {bio}"
    )

    try:
        print(f"{datetime.now()}. Running classification...")
        result = await classify_message(text, bio)
        print(
            f"@{settings.telegram_chat} is lead"
            if result["lead"]
            else f"@{settings.telegram_chat} is not lead"
        )
        print()
    except httpx.ConnectError as e:
        print(
            f"Classificaion failed. Start fastapi container first and access from port, specified in the env file."
        )
        print()
