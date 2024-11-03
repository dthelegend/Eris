import serial
import time

# Specify the serial port and baud rate (make sure they match the Arduino sketch)
arduino_port = "COM3"  # Change this to your Arduino's serial port
baud_rate = 9600

# Open the serial connection
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Wait for the connection to initialize

def send_command(command):
    """Send a command to the Arduino."""
    ser.write(command.encode())
    print(f"Sent command: {command}")

def read_command():
    """Read incoming commands from the Arduino."""
    if ser.in_waiting > 0:
        incoming = ser.readline().decode().strip()
        print(f"Received from Arduino: {incoming}")
        if incoming == "GO":
            print("LIGHTS OUT")
            return False
        
    return True
    

def main():
    send_command("LIGHTS")
    while read_command():
        pass
    send_command("WAVE")