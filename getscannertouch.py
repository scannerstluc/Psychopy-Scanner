from psychopy import visual, event, core
import serial
win = visual.Window(fullscr=True)
event.globalKeys.add(key='escape', func=win.close)
ser = serial.Serial('COM3', 9600)
while True:
    trigger = ser.read().decode()
    print(f"Trigger received: {trigger}")
    if trigger == "o":
        print("test concluant")