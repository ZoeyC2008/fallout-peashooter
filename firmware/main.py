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
button_pressed = False

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
    global current_angleY
    yValue = get_centered(y_axis)
    if yValue != 0:
        button_pressed = False
    

    setangleY = setLimAngle(current_angleY - yValue**3 * servoY_speed/24)
    servoY.angle = setangleY
    current_angleY = setangleY
    
    
def set_yaw():
    global current_angleX

    xValue = get_centered(x_axis)

    if xValue != 0:
        button_pressed = False
    
    setanglex = setLimAngle(current_angleX - xValue**3 * servoX_speed/24)
    servoX.angle = setanglex
    current_angleX = setanglex
    print(current_angleX)
    
def check_button():
    global button_pressed
    buttonValue = not (button.value)
    
    if buttonValue == 1 and button_pressed == False:
        button_pressed = True
        
        
    elif buttonValue == 1 and button_pressed == True:
        button_pressed = False
        
    while button.value == 0:
            print("button pressed")
            time.sleep(0.05)
        


# Sweep servo from 0 to 180 degrees

    
while True:
    set_pitch()
    set_yaw()
    check_button()
    # dc_motor.throttle = 0.7


    if button_pressed:
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
    print(f"button_pressed: {button_pressed}  button.value: {buttonvalue}")

    time.sleep(0.01)
    