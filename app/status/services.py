from httpx import AsyncClient, RequestError
import asyncio


async def check_http(service):
    async with AsyncClient() as client:
        try:
            r = await client.get(service["url"])
            return "Healthy" if r.status_code == 200 else "Degraded"

        except RequestError:
            return "Degraded"


async def check_tcp(service):
    try:
        reader, writer = await asyncio.open_connection(service["host"], service["port"])
        writer.close()
        await writer.wait_closed()
        return "Healthy"
    except Exception:
        return "Degraded"
