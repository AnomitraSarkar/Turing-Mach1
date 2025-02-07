# import pygame package 
import pygame 
from torch import *
import csv
  
# functions
def append_file(writer):
    with open(f'{writer}', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

# initializing imported module 
class Playground(): 
    def __init__(self, winsize=(400, 500)):
        self.winsize = winsize
        pygame.init() 
        self.screen = pygame.display.set_mode(self.winsize) 
        self.target = None
        self.geometry = None
        
    def init_target(self):
        if self.target is None or self.target < (0,0) or self.target > self.winsize:
            pass
        else:
            pygame.draw.circle(self.screen, (255,0,0), (self.target[0], self.target[1]), 5)
            print(self.target)
            pygame.display.update()
    
    def init_machine(self):
        if self.geometry is None:
            pass
        else:
            for i in range(0,len(self.geometry)):
                print(i)
                pygame.draw.line(self.screen, self.geometry[i][0], self.geometry[i][1], self.geometry[i+1][1], 5)
        pygame.display.flip()
    
    def run(self):
        clock=pygame.time.Clock()
        counter = 0
        running = True
        
        while running: 
            pygame.display.update()
            clock.tick(1)
            counter += 1
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False
            self.init_target()
            self.init_machine()
            pygame.display.update()
        pygame.quit()
        
    def set_target(self, point):
        self.target = point
        
    def set_machine(self, geometry):
        self.geometry = geometry
        
if __name__ == "__main__":
    env = Playground()
    env.set_target(point=(200,200))
    env.set_machine(
        [
            ((255,0,0), (300,400)),
            ((255,0,0), (300,300)),
            ((255,0,0), (300,200)),
        ]
    )
    env.run()
