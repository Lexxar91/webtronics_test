import aiohttp

kickbox_api_key = "live_3e97967c75d0b29fd71c13a25b02afb36e8caa71d8ccbe0d71d312f3bb74e305"


async def check_email_async(email):
    url = "https://api.kickbox.com/v2/verify"
    params = {"email": email, "apikey": kickbox_api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()
