import asyncio

import serial

class ArduinoStuff:
    def __init__(self):
        # Specify the serial port and baud rate (make sure they match the Arduino sketch)
        # arduino_port = "COM3"  # Change this to your Arduino's serial
        arduino_port = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_950333130313511022F0-if00"
        baud_rate = 9600

        # Open the serial connection
        self.ser = serial.Serial(arduino_port, baud_rate)

    def send_command(self, command):
        """Send a command to the Arduino."""
        self.ser.write(command.encode())
        print(f"Sent command: {command}")

    def read_command(self):
        """Read incoming commands from the Arduino."""
        if self.ser.in_waiting > 0:
            incoming = self.ser.readline().decode().strip()
            print(f"Received from Arduino: {incoming}")
            if incoming == "GO":
                print("LIGHTS OUT")
                return False

        return True

    async def lez_go(self):
        self.send_command("LIGHTS")
        while self.read_command():
            await asyncio.sleep(0.1)
        return

    def done(self):
        self.send_command("WAVE")