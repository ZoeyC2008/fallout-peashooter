import board
import pwmio
import time
import digitalio
import analogio
from adafruit_motor import servo, motor

# Define the PWM pin connected to the servo's signal wire

servoX_pin = pwmio.PWMOut(board.D4, frequency=50)
servoX_pin.duty_cycle = (int) (2 ** 15)
servoY_pin = pwmio.PWMOut(board.D6, frequency=50)
servoX_pin.duty_cycle = (int) (2 ** 15)
dc_pin1 = pwmio.PWMOut(board.D8, frequency=20000)
dc_pin2 = pwmio.PWMOut(board.D9, frequency=20000)


x_axis = analogio.AnalogIn(board.A0)
y_axis = analogio.AnalogIn(board.A1)

button = digitalio.DigitalInOut(board.D5)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

pot = analogio.AnalogIn(board.A2)

def round_analog(pin):
    return (int) (pin.value / (64*64))

def get_centered(pin):
    # raw is 0-65535, /64 -> 0-1023-ish, then center around 0
    return round_analog(pin) - 8
# potentiometer = analogio.AnalogIn(board.GP26)

current_angleX = 90.0
servoX_speed = 0.15
current_angleY = 90.0
servoY_speed = 0.15
button_toggled = False

xValue = 0
yValue = 0

# Create a servo object
servoX = servo.Servo(servoX_pin, min_pulse=500, max_pulse=2500)
servoY = servo.Servo(servoY_pin, min_pulse=500, max_pulse=2500)
 # Create a servo object


# Initialize the motor object for Channel A
dc_motor = motor.DCMotor(dc_pin1, dc_pin2)


def setLimAngle(angle):
    return max(min(angle, 135),45)
    
def set_pitch():
    global current_angleY, button_toggled 
    yValue = get_centered(y_axis)
    if yValue != 0:
        button_toggled = False
    

    current_angleY = setLimAngle(current_angleY - yValue**3 * servoY_speed/24)
    servoY.angle = current_angleY 
    
    
def set_yaw():  
    global current_angleX, button_toggled

    xValue = get_centered(x_axis)

    if xValue != 0:
        button_toggled = False
    
    current_angleX = setLimAngle(current_angleX - xValue**3 * servoX_speed/24)
    servoX.angle = current_angleX

    # print(current_angleX)
    
def check_button():
    global button_toggled
    buttonPressed = not (button.value)
    
    if buttonPressed:
        button_toggled = not button_toggled
        
        while button.value == 0:
                print(f"button pressed {button_toggled}")
                time.sleep(0.1)
        

# Sweep servo from 0 to 180 degrees
 
while True:
    set_pitch()
    set_yaw()
    check_button()
    # dc_motor.throttle = 0.7


    if button_toggled:

        dc_motor.throttle = round_analog(pot)/15*0.3+0.7# pot reading
    
    else:
        dc_motor.throttle = 0

    buttonvalue = not button.value
    
    # for angle in range(0, 181, 1):
    #     servoX.angle = angle
    #     time.sleep(0.0)
    # print("1")
    # time.sleep(1)
    # for angle in range(180, -1, -1):
    #     servoX.angle = angle
    #     time.sleep(0.0)
    # print("2")
    # time.sleep(1)

    # xValue = get_centered(x_axis)
    # yValue = get_centered(y_axis)
    # potVal = round_analog(pot)
    # buttonValue = button.value  # True = not pressed, False = pressed

    # print(f"X: {xValue:7.0f}  Y: {yValue:7.0f}  Button: {'PRESSED' if not buttonValue else 'released'} Pot: {potVal:7.0f}")
    print(f"button_toggled: {button_toggled}  button.value: {buttonvalue}")

    time.sleep(0.01)
    