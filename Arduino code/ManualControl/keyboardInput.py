import serial
from pynput import keyboard
from timeit import default_timer as timer

# Configure your COM port and baud rate
COM_PORT = '/dev/ttyACM0'  # Change this to your COM port
BAUD_RATE = 115200   # Change this to match your UART device configuration

# Open the serial connection
ser = serial.Serial(COM_PORT, BAUD_RATE)

pos = 0
ser.write(str(int(pos)).encode('utf-8'))

# Multiplier to comand constant rotation speed of servo
# 1 is slow
vel_mult = 2

def on_press(key):
    # print("press", key)
    # if ser.in_waiting == 0:
    change = 0
    if key == keyboard.Key.up:
        change += 1
    if key == keyboard.Key.down:
        change -= 1
    global pos
    pos += change*vel_mult
    ser.write(str(int(pos)).encode('utf-8'))
    

def on_release(key):
    return
    # print("release")

listener = keyboard.Listener(on_press=on_press, on_release=on_release)


try:
    listener.start()
    while True:
        if ser.in_waiting > 0:
            c = ser.readline()
            print(c.decode('utf-8').replace('\n',''))

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()