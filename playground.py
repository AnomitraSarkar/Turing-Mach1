import pygame 
import csv
from math import sin, cos, sqrt, radians
from random import random


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Perceptron:
    def __init__(self, neurons_count):
        self.neurons = neurons_count
        self.weights = [random() for i in self.neurons]
        




# Function to append to CSV
def append_file(writer, headers, data):
    file_exists = False
    try:
        with open(writer, 'r') as csvfile:
            rows = list(csv.reader(csvfile))
            file_exists = bool(rows)
            last_row = rows[-1] if rows else None
    except FileNotFoundError:
        last_row = None
    
    if last_row and last_row == data:
        return  # Avoid appending duplicate last value
    
    with open(writer, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if not file_exists:
            csv_writer.writerow(headers)
        csv_writer.writerow(data)

# Function to calculate distance
def distance(coord1, coord2):
    return sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Playground Class
class Playground(): 
    def __init__(self, winsize=(900, 600)):
        pygame.init()  # Initialize pygame first
        self.font = pygame.font.Font(None, 36)  # Load font AFTER pygame.init()
        self.winsize = winsize
        self.screen = pygame.display.set_mode(self.winsize) 
        pygame.display.set_caption("Machine Target Simulation")
        self.target = None
        self.geometry = None
        self.angles = [0, 0, 0]  # Individual angles for each joint
        self.state = "Initiating Controllable"
        self.q_table = {
            "Loss":winsize[0]*winsize[1],
            "Angles": self.angles
        }
        self.acceptance_limit = 10
        self.gradients = []
        

    def init_target(self):
        """Draw the target point."""
        if self.target is not None and (0 <= self.target[0] < self.winsize[0]) and (0 <= self.target[1] < self.winsize[1]):
            pygame.draw.circle(self.screen, BLUE, (self.target[0], self.target[1]), 5)

    def init_machine(self):
        
        for i in range(len(self.angles)):
            if self.angles[i] > 360:
                self.angles[i] -= 360
            elif self.angles[i] < -360:
                self.angles[i] += 360
        
        """Draw the machine arm with joints."""
        
        if self.geometry is None:
            return
        
        for i in range(len(self.geometry) - 1):
            pygame.draw.line(self.screen, self.geometry[i][0], self.geometry[i][1], self.geometry[i+1][1], 5)
            pygame.draw.circle(self.screen, GREEN, self.geometry[i][1], 4)
        pygame.draw.circle(self.screen, GREEN, self.geometry[-1][1], 5)

        # Update the joint positions
        original_lengths = [
            distance(self.geometry[i][1], self.geometry[i+1][1]) for i in range(len(self.geometry) - 1)
        ]
        
        for i in range(len(self.geometry) - 1):
            cx, cy = self.geometry[i][1]
            angle = radians(self.angles[i])
            new_x = cx + original_lengths[i] * cos(angle)
            new_y = cy + original_lengths[i] * sin(angle)
            self.geometry[i+1][1] = [new_x, new_y]

    def reset_env(self,counter,mod):
        if counter%mod==0:
            self.angles[0] = int(random()*360)
        if counter%mod==0:
            self.angles[1] = int(random()*360)
        for i in self.gradients:
            pygame.draw.circle(self.screen, GREEN, i, 5)
            pygame.display.flip()

    def calculate_q_table(self):
        if distance(self.geometry[-1][-1],self.target)<self.q_table["Loss"]:
            self.q_table["Angles"] = self.angles[:]  # Shallow copy to prevent reference issues
            print("Understood")
            self.gradients.append(self.geometry[-1][-1])
            self.q_table["Loss"] = distance(self.geometry[-1][-1],self.target)
            self.state = f"{self.q_table["Loss"]}"
            
    def run(self):
        """Main loop for running the simulation."""
        clock = pygame.time.Clock()
        running = True
        FPS = 120
        counter = 0
        
        while running:             
            clock.tick(FPS)
            counter+=1
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False                                     
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.angles[0] += 0.5
            if keys[pygame.K_RIGHT]:
                self.angles[0] -= 0.5
            if keys[pygame.K_UP]:
                self.angles[1] += 0.5
            if keys[pygame.K_DOWN]:
                self.angles[1] -= 0.5

            if self.acceptance_limit>=self.q_table["Loss"]:
                self.angles = self.q_table["Angles"]
                self.reset_env(1, 10)
                self.state = "Final Config: " + f"{int(self.q_table["Loss"])}"
            else:
                self.reset_env(counter,2)
            self.screen.fill(WHITE)
            self.init_target()
            self.init_machine()
            self.calculate_q_table()

            # Display text
            text = self.font.render(self.state, True, RED)  
            text_rect = text.get_rect(center=(700, 50))  
            self.screen.blit(text, text_rect) 
            
            text = self.font.render(f"Iteration: {counter}", True, GREEN)  
            text_rect = text.get_rect(center=(700, 25))  
            self.screen.blit(text, text_rect) 

            print(self.angles, self.q_table)
            
                

            # Append data to file
            if self.geometry and self.target:
                append_file(
                    f"target-{self.target}-def-mach-config.csv",
                    ["X0", "Y0", "X1", "Y1", "XF", "YF", "Angle0", "Angle1", "TargetX", "TargetY"],
                    [self.geometry[0][1][0], self.geometry[0][1][1], 
                     self.geometry[1][1][0], self.geometry[1][1][1], 
                     self.geometry[2][1][0], self.geometry[2][1][1], 
                     self.angles[0], self.angles[1], self.target[0], self.target[1]]
                )

            pygame.display.flip()
        
        pygame.quit()
    
    def set_target(self, point):
        """Set the target coordinates."""
        self.target = point

    def set_machine(self, geometry):
        """Set the machine's joint positions."""
        self.geometry = geometry

# Run the simulation
if __name__ == "__main__":
    mach_config = [
        [RED, [300, 400]],
        [RED, [300, 300]],
        [RED, [300, 200]],
    ]
    env = Playground()
    env.set_target(point=(325, 325))
    env.set_machine(mach_config)
    env.run()
