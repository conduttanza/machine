#05/02/2026

from config import Config
config = Config()
from window import Window
import pigpio
from threading import Thread
import time
    
class Move():
    def __init__(self, window):
        self.window = window
        self.pi = pigpio.pi()
        if not self.pi.connected:
            exit()
        self.PWM = 16
        self.AIN1 = 20
        self.AIN2 = 21
        for pin in (self.AIN1, self.AIN2):
            self.pi.set_mode(pin, pigpio.OUTPUT)
        self.delay =  config.delay
        self.pi.set_PWM_frequency(self.PWM,1000)
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        while True:
            if getattr(self.window, 'move', False):
                self.moveFwd()
                self.window.move = False
            time.sleep(config.delay)
    
    def moveFwd(self):
        print('moving huh')
        self.pi.write(self.AIN1, 1)
        self.pi.write(self.AIN2, 0)
        self.pi.set_PWM_dutycycle(self.PWM,32)
        time.sleep(config.delay)
        self.stop()

    def stop(self):
        self.pi.set_PWM_dutycycle(self.PWM,0)
        self.pi.write(self.AIN1, 0)
        self.pi.write(self.AIN2, 0)

# Create window first but DON'T start main() yet
window = Window.__new__(Window)
window.running = True
window.move = False
import pygame
pygame.init()
pygame.display.set_caption('motor movement')
window.screen = pygame.display.set_mode((600,600))
window.clock = pygame.time.Clock()

# NOW create Move with the window reference
move = Move(window)

# FINALLY run the blocking Pygame loop
window.main()

