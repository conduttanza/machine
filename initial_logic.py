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
                self.speed = getattr(self.window, 'speed', 8)
                if self.speed > 0:
                    self.moveFwd()
                elif self.speed < 0:
                    self.moveBack()
            if getattr(self.window, 'move') == False:
                self.stop()
            time.sleep(config.delay)
    
    def moveFwd(self):
        self.pi.write(self.AIN1, 1)
        self.pi.write(self.AIN2, 0)
        self.pi.set_PWM_dutycycle(self.PWM,self.speed)
    
    def moveBack(self):
        self.pi.write(self.AIN1,0)
        self.pi.write(self.AIN2,1)
        self.pi.set_PWM_dutycycle(self.PWM,-self.speed)

    def stop(self):
        self.pi.set_PWM_dutycycle(self.PWM,0)
        self.pi.write(self.AIN1, 0)
        self.pi.write(self.AIN2, 0)
    
    def cleanUp(self):
        self.pi.stop()

window = Window.__new__(Window)
window.running = True
window.move = False
import pygame
pygame.init()
pygame.display.set_caption('motor movement')
window.screen = pygame.display.set_mode((600,600))
window.clock = pygame.time.Clock()
move = Move(window)

window.main()


