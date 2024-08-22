from psychopy import visual, event, core
import serial


texte = "appuyez sur les boutons"


win = visual.Window(fullscr=True)
ser = serial.Serial('COM2', 9600)
trigger = ser.read().decode('utf-8')
while trigger != 's':
    trigger = ser.read().decode('utf-8')
stim = visual.TextStim(win, text=texte, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font='Arial')
stim.draw()
win.flip()


event.globalKeys.add(key='escape', func=win.close)
timer = core.Clock()
timer.reset()
while timer.getTime()<40:
    trigger = ser.read().decode()
    print(f"Trigger received: {trigger}")
win.close()
core.quit()
