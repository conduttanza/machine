#07/02/2026

from config import Config
config = Config()
from window import Window
from threading import Thread
import time
    
class Move_not_pi():
    def __init__(self, window):
        print('not pi')
        self.window = window
        self.delay =  config.delay
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        self.speed = 0
        while True:
            if getattr(self.window, 'move', False):
                self.speed = getattr(self.window, 'speed', 8)
                #print(f'self.speed = {self.speed}')
                if self.speed >= 0:
                    self.moveFwd()
                elif self.speed < 0:
                    self.speed = -self.speed
                    self.moveBack()
            if getattr(self.window, 'move') == False:
                actSpeed = getattr(self,'speed')
                if actSpeed < 0:
                    self.speed = -self.speed
                    self.moveBack()
                else:
                    self.moveFwd()
                self.speed -= 4
                if -8 < actSpeed < 8:
                    self.stop()
                    self.speed = 0
            time.sleep(config.delay)
    
    def moveFwd(self):
        #print('moving fwd')
        print(f'speed: {self.speed}')
    
    def moveBack(self):
        #print('moving bwd')
        print(f'speed: {self.speed}')

    def stop(self):
        pass#print('idle')
        

window = Window.__new__(Window)
window.running = True
window.move = False
import pygame
pygame.init()
pygame.display.set_caption('motor movement')
window.screen = pygame.display.set_mode((600,600))
window.clock = pygame.time.Clock()
move = Move_not_pi(window)

window.main()

