import pygame
from threading import Thread
from config import Config
config = Config()

class Window():
    def __init__(self):
        self.running = True
        pygame.init()
        pygame.display.set_caption('motor movement')
        self.screen = pygame.display.set_mode((600,600))
        self.clock = pygame.time.Clock()
        Thread(target=self.windowUpdate, daemon=False).start()
    
    def windowUpdate(self):
        if config.App == True:
            self.main()
    
    def main(self):
        try:
            button = pygame.rect(150,100,100,150)
            while self.running: 
                self.screen.fill(255,255,255)
                pygame.draw.rect(self.screen, (0,255,0), button)
                for event in pygame.event.get():
                    if event == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button.collidepoint(event.pos):
                            self.returnTrue()
                
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()
    
    def returnTrue(self):
        return True

Window()