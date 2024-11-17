import serial
import time

# Replace 'COM3' with the appropriate port for your system
ser = serial.Serial('COM6', 115200, timeout=1)
time.sleep(2)  # Wait for the connection to establish

def send_data(data):
    ser.write(data.encode())

def receive_data():
    return ser.readline().decode().strip()

send_data('Hello ESP32')


