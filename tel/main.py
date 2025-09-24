from tel.handlers import client
from tel.config import settings


async def main():

    await client.start(phone=settings.telegram_phone)
    await client.run_until_disconnected()


if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
