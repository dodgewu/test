from NTL7465LG_8063 import test_8063
import asyncio

async def main():
    ip="172.16.42.157"
    await test_8063(ip)

asyncio.run(main())