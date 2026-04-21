import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        r = await client.get('http://localhost:8000/', timeout=10.0)
        print(f'Status: {r.status_code}')
        print(f'Response: {r.json()}')

asyncio.run(test())
