import asyncio

def scan():
    async def scan_main():
        import anki

        # This object handles all the connections to the vehicles
        controller = anki.Controller()
        # This simplifies connecting to multiple vehicles a lot
        vehicles = await controller.connect_many(2)

        # `vehicles` is a tuple, meaning we can iterate over it like this
        for v in vehicles:
            print(f"Found car@{v.id}")

    asyncio.run(scan_main())

def test():
    async def test_main():
        import anki

        # This object handles all the connections to the vehicles
        controller = anki.Controller()
        # This simplifies connecting to multiple vehicles a lot
        vehicles = await controller.connect_many(2)

        # `vehicles` is a tuple, meaning we can iterate over it like this
        for v in vehicles:
            await v.set_speed(300)
        await asyncio.sleep(10)
        for v in vehicles:
            await v.stop()

        # This is a short hand for disconnecting from multiple vehicles
        await controller.disconnect_all()

    asyncio.run(test_main())
