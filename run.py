#05/02/2026
from config import Config
config = Config()
from window import Window
import pygame

# 0 if you dont have a raspberry pi connected
# else 1
pi = 1

if pi == True:
    from initial_logic import Motor, Servo
else:
    from debug import Motor_not_pi as Motor, Servo_not_pi as Servo

#setup pygame window
window = Window.__new__(Window)
window.running = True
window.move = False
pygame.init()
pygame.display.set_caption('motor movement')
window.screen = pygame.display.set_mode((600,600))
window.clock = pygame.time.Clock()

if config.motorRun == True:
    motor = Motor(window)
if config.servoRun == True:
    servo = Servo(window)

window.main()