from eris.consts import GROUND_SHOCK, SKULL


def scan():
    print("hello, world")
    pass

def test():
    from overdrive import Overdrive

    def locationChangeCallback(addr, params):
        # Print out addr, piece ID, location ID of the vehicle, this print everytime when location changed
        print("Location from {addr} : Piece={piece} Location={location} Clockwise={clockwise}".format(addr=addr,
                                                                                                    **params))

    cars = [Overdrive(GROUND_SHOCK), Overdrive(SKULL)]
    for car in cars:
        car.setLocationChangeCallback(locationChangeCallback)  # Set location change callback to function above
        car.changeSpeed(1000, 500)  # Set car speed with speed = 500, acceleration = 500
        car.changeLaneLeft(500, 500)  # Switch to next right lane with speed = 500, acceleration = 500
    input("Done.")  # Hold the program so it won't end abruptly

