import random
from time import sleep

from anki.misc.const import TrackPieceType

import asyncio
from anki import Vehicle, Controller, Lane4

NUM_LAPS = 5

class RaceCar:
    def __init__(self, car: Vehicle):
        self.car = car
        self.lap_number = 0

    async def start(self):
        await self.car.set_speed(600)

        while True:
            if random.random() < 0.1:
                new_lane = random.choice(list(Lane4))
                await self.car.change_lane(new_lane, 900)
                print(f"car@{self.car.id} has changed lane to Lane@{new_lane}")
            current_track = await self.car.wait_for_track_change()
            print(f"Current Track@{current_track}")
            if current_track.type == TrackPieceType.FINISH:
                self.lap_number += 1
            if self.lap_number > NUM_LAPS:
                await self.car.stop()

    @staticmethod
    async def main(num_cars_to_connect = 2):
        controller = Controller()

        if num_cars_to_connect > 4:
            raise ValueError("Too many cars to connect")
        elif num_cars_to_connect == 0:
            raise ValueError("No cars to connect")

        print(f"Drivers are putting on their helmets...")
        vehicles = await controller.connect_many(num_cars_to_connect)

        print(f"Drivers are lining up...")
        map = await controller.scan()

        await asyncio.gather(*(vehicle.align() for vehicle in vehicles))

        race_ready_cars : list[RaceCar] = [RaceCar(args) for args in vehicles]

        await asyncio.gather(*(car.start() for car in race_ready_cars))

        await controller.disconnect_all()

        print("Start")
