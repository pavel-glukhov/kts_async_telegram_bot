import aiohttp
import json


async def fetch_10() -> list[float]:
    result = []
    async with aiohttp.ClientSession() as session:
        ws = await session.ws_connect('wss://ws.bitmex.com/realtime?subscribe=instrument:XBTUSD')
        async for msg in ws:
            data = json.loads(msg.data).get('data')
            if data:
                if price := data[0].get('fairPrice'):
                    result.append(price)
                if len(result) == 10:
                    break

    return result
