import asyncio
async def main():
    i=0
    while i<5:
        print("ss")
        await asyncio.sleep(1)
        print(i)
        i+=1
asyncio.run(main())