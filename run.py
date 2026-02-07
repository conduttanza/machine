#05/02/2026
from config import Config
config = Config()

pi = 1
if pi == True:
    from initial_logic import Motor, Servo
    if config.motorRun == True:
        Motor()
        Motor.cleanUp()
    if config.servoRun == True:
        Servo()
elif pi == False:
    from debug import Motor_not_pi, Servo_not_pi
    if config.motorRun == True:
        Motor_not_pi()
    if config.servoRun == True:
        Servo_not_pi()