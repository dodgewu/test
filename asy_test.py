import asyncio

async def main():
    print("hello")
    await asyncio.sleep(1)
    print("world")


loop=asyncio.get_event_loop()
my_task=loop.create_task(main())
loop.run_until_complete(my_task)
