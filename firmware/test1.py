import board
import pwmio
import time
import digitalio
import analogio
from adafruit_motor import servo, motor


x_axis = analogio.AnalogIn(board.A0)
y_axis = analogio.AnalogIn(board.A1)
button = digitalio.DigitalInOut(board.D5)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

while True: 
    print("x_axis:"+x_axis.value + ", y axis: " + y_axis.value + ", button pressed: " + button.value)
