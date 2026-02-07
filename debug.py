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
        while True:
            if getattr(self.window, 'move', False):
                self.moveFwd()
            if getattr(self.window, 'move') == False:
                self.stop()
            time.sleep(config.delay)
    
    def moveFwd(self):
        #print('moving')
        speed = getattr(self.window, 'speed', 0)
        print(f'speed: {speed}')

    def stop(self):
        print('idle')
        

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

