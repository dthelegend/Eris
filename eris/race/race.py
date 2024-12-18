import random
from time import sleep

from anki.misc.const import TrackPieceType

import asyncio
from anki import Vehicle, Controller, Lane4
from httpx import stream

import eris.lights
from eris.stream import FormulaCamera

NUM_LAPS = 5
HARVESTSPEED = 600
NORMALSPEED = 800
HIGHSPEED = 1000

class BasicAgent:
    def __init__(self):
        self.energy = 50
    
    def act(self, lap_number, opponent_distance, opponent_lane, current_lane, current_piece_type): #Basic Agent
        desired_speed = NORMALSPEED #base
        if self.lap_number == NUM_LAPS-1:
            #Last lap, go all out!
            desired_speed = HIGHSPEED
        else:
            if opponent_distance < 1:
                desired_speed = HIGHSPEED
            elif opponent_distance > 2 and self.energy < 50:
                desired_speed = HARVESTSPEED
            elif self.energy > 80:
                desired_speed = HIGHSPEED
            elif self.energy < 30:
                desired_speed = HARVESTSPEED
            else:
                desired_speed = NORMALSPEED
            
        if self.energy <= 0 and desired_speed == HIGHSPEED:
            desired_speed = NORMALSPEED

        if desired_speed == HIGHSPEED:
            self.energy -= 5
        elif desired_speed == HARVESTSPEED:
            self.energy += 8
        
        if current_piece_type == TrackPieceType.CURVE:
            desired_speed -= 100

        return (desired_speed, (current_lane == opponent_lane) and desired_speed == HIGHSPEED)
            


class RaceCar:
    def __init__(self, car: Vehicle):
        self.car = car
        self.lap_number = 0
        self.car.on_track_piece_change = self.on_track_piece_change
        self.position = 0

    def on_track_piece_change(self):
        if self.car.current_track_piece.type == TrackPieceType.FINISH:
            self.lap_number += 1
        self.position = self.car.map_position * 100 // len(self.car.map)

    async def start(self):
        await self.car.set_speed(800)

    async def mainloop(self):
        if random.random() < 0.01:
            new_lane = random.choice(list(Lane4))
            await self.car.change_lane(new_lane, 200)
            print(f"car@{self.car.id} has changed lane to Lane@{new_lane}")

    async def stop(self):
        await self.car.stop()

    @staticmethod
    async def main(num_cars_to_connect = 2, run_stream = False, run_lights = False, run_crofty = False):
        controller = Controller()

        try:
            if num_cars_to_connect > 4:
                raise ValueError("Too many cars to connect")
            elif num_cars_to_connect == 0:
                raise ValueError("No cars to connect")

            print(f"Drivers are putting on their helmets...")
            vehicles = await controller.connect_many(num_cars_to_connect)

            lights = None
            if run_lights:
                lights = eris.lights.ArduinoStuff()

            crofty = None
            if run_crofty:
                crofty = eris.crofty.Crofty()
                asyncio.create_task(crofty.race_start())

            print(f"Drivers are lining up...")
            _map = await controller.scan()

            await asyncio.gather(*(car.align() for car in vehicles))

            await asyncio.sleep(5)

            if run_lights:
                await lights.lez_go()

            race_ready_cars : list[RaceCar] = [RaceCar(args) for args in vehicles]
            stream = None
            if run_stream:
                stream = FormulaCamera()
                stream.maxlaps = NUM_LAPS

            start_tasks = [car.start() for car in race_ready_cars]

            if run_crofty:
                asyncio.create_task(crofty.lights_out())

            await asyncio.gather(*start_tasks)
            has_waved = False
            while ((current_lap := max(car.lap_number for car in race_ready_cars)) <= NUM_LAPS) and (not run_stream or stream.display()):
                await asyncio.gather(*(car.mainloop() for car in race_ready_cars))
                if run_stream:
                    stream.update_progress_all([car.position for car in race_ready_cars])
                    stream.update_distance_all([car.position + car.lap_number*100 for car in race_ready_cars])
                    stream.set_lap(current_lap)
                if run_lights and (not has_waved) and (current_lap + 1 > NUM_LAPS):
                    has_waved = True
                    lights.done()
                    if run_crofty:
                        asyncio.create_task(crofty.last_lap())

                await asyncio.sleep(1 / 60)

            if run_crofty:
                asyncio.create_task(crofty.victory(max((idx, car.lap_number, car.position) for idx, car in enumerate(race_ready_cars))[0] == 0))
            await asyncio.gather(*(car.set_speed(300) for car in vehicles))
            await asyncio.sleep(3)
            await asyncio.gather(*(car.align() for car in vehicles))
            await asyncio.gather(*(car.stop() for car in race_ready_cars))

            await controller.disconnect_all()
        except Exception as e:
            await controller.disconnect_all()
            raise e