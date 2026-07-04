import board
import pwmio
import time
import digitalio
import analogio
from adafruit_motor import servo, motor

# Define the PWM pin connected to the servo's signal wire
# (Change to board.D12 or your specific board's pin)
servoX_pin = pwmio.PWMOut(board.D4, frequency=50)
servoY_pin = pwmio.PWMOut(board.D6, frequency=50)
dc_pin1 = pwmio.PWMOut(board.D13, frequency=2000)
dc_pin2 = pwmio.PWMOut(board.D13, frequency=2000)

# Define the sleep pin and enable the driver 
sleep_pin = digitalio.DigitalInOut(board.D6)
sleep_pin.direction = digitalio.Direction.OUTPUT
sleep_pin.value = True

x_axis = analogio.AnalogIn(board.A0)
y_axis = analogio.AnalogIn(board.A1)
button = digitalio.DigitalInOut(board.GP14)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# potentiometer = analogio.AnalogIn(board.GP26)

current_angleX = 90
servoX_speed = 0.5
current_angleY = 90
servoY_speed = 0.5
button_pressed = False

xValue = 0
yValue = 0

# Create a servo object
servoX = servo.Servo(servoX_pin, min_pulse=500, max_pulse=2500)
servoY = servo.Servo(servoY_pin, min_pulse=500, max_pulse=2500)

# Initialize the motor object for Channel A
dc_motor = motor.DCMotor(dc_pin1, dc_pin2)

    
def set_pitch():
    yValue = y_axis.value/64 - 511 # convert to [-511, 511]
    if yValue != 0:
        button_pressed = False
    current_angleY = current_angleY - yValue * servoY_speed
    servoY.angle = current_angleY
    
def set_yaw():
    xValue = x_axis.value/64 - 511 # convert to [-511, 511]
    if xValue != 0:
        button_pressed = False
    current_angleX = current_angleX - xValue * servoX_speed
    servoX.angle = current_angleX
    
def check_button():
    buttonValue = button.value
    
    if buttonValue == 0 and button_pressed == False and xValue==511 and yValue==511:
        button_pressed = True
        
    elif buttonValue == 0 and button_pressed == True:
        button_pressed = False
        
 
    
while True:
    set_pitch()
    set_yaw()
    
    # if button_pressed:
    #     dc_motor.throttle = # pot reading

    time.sleep(0.2)