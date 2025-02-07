# import pygame package 
import pygame 
import csv
from math import sin, cos, pi, sqrt, radians
  
# functions
def append_file(writer):
    with open(f'{writer}', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
def distance(coord1 , coord2):
    return sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
    

# initializing imported module 
class Playground(): 
    def __init__(self, winsize=(900, 600)):
        self.winsize = winsize
        pygame.init() 
        self.screen = pygame.display.set_mode(self.winsize) 
        self.target = None
        self.geometry = None
        self.angle = [0, 0, 0]
        
    def init_target(self):
        if self.target is None or self.target < (0,0) or self.target > self.winsize:
            pass
        else:
            pygame.draw.circle(self.screen, (255,0,0), (self.target[0], self.target[1]), 5)
            pygame.display.update()
    
    def init_machine(self):
        if self.geometry is None:
            pass
        else:
            for i in range(0,len(self.geometry)-1):
                pygame.draw.line(self.screen, self.geometry[i][0], self.geometry[i][1], self.geometry[i+1][1], 5)
            print(self.geometry)
            for i in range(len(self.geometry)-1):
                xnew = cos(self.angle[i])*( distance(self.geometry[i+1][1] , self.geometry[i][1])) + self.geometry[i][1][0]
                ynew = sin(self.angle[i])*( distance(self.geometry[i+1][1] , self.geometry[i][1])) + self.geometry[i][1][1]
                self.geometry[i+1][1][0],self.geometry[i+1][1][1]=xnew,ynew
            
        pygame.display.flip()
    
    def run(self):
        clock=pygame.time.Clock()
        counter = 0
        running = True
        FPS = 60
        
        while running: 
            clock.tick(FPS)
            counter += 1
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.angle[1] += 0.5
            if keys[pygame.K_RIGHT]:
                self.angle[1] -= 0.5
                
                
                
            self.screen.fill((0,0,0))
            self.init_machine()
            pygame.display.update()
        pygame.quit()
        
    def set_target(self, point):
        self.target = point
        
    def set_machine(self, geometry):
        self.geometry = geometry
        
if __name__ == "__main__":
    mach_config = [
            [[255,0,0], [300,400]],
            [[255,0,0], [300,300]],
            [[255,0,0], [300,200]],
        ]
    env = Playground()
    env.set_target(point=(200,200))
    env.set_machine(
        mach_config
    )
    env.run()
    
