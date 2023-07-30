import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

kickbox_api_key = os.getenv("KICKBOX_API_KEY")


async def check_email_async(email: str) -> dict:
    url = "https://api.kickbox.com/v2/verify"
    params = {"email": email, "apikey": kickbox_api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()
