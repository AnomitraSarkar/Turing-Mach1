import pygame 
import csv
import torch
import torch.nn as nn
import torch.optim as optim
from math import sin, cos, sqrt, radians
import numpy as np
  
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
  
# Neural Network for Angle Prediction
class AnglePredictor(nn.Module):
    def __init__(self):
        super(AnglePredictor, self).__init__()
        self.fc1 = nn.Linear(6, 15)  # Input: (TargetX, TargetY, FX, FY, A0, A1)
        self.fc2 = nn.Linear(15, 6)  # Output: (Angle0, Angle1)
        self.leaky_relu = nn.LeakyReLU()
        
    def forward(self, x):
        x = self.leaky_relu(self.fc1(x))
        x = self.fc2(x)
        return x
  
# Functions
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
        
def distance(coord1, coord2):
    return sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
    
# Initializing imported module 
class Playground(): 
    def __init__(self, winsize=(900, 600)):
        self.winsize = winsize
        pygame.init() 
        self.screen = pygame.display.set_mode(self.winsize) 
        self.target = None
        self.geometry = None
        self.angles = [-10, -130, 0]  # Individual angles for each joint
        
        # Initialize neural network and optimizer
        self.model = AnglePredictor()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.criterion = nn.HuberLoss(reduction='mean', delta=1.0)
        
    def init_target(self):
        if self.target is None or not (0 <= self.target[0] < self.winsize[0] and 0 <= self.target[1] < self.winsize[1]):
            pass
        else:
            pygame.draw.circle(self.screen, BLUE, (self.target[0], self.target[1]), 5)
            pygame.display.update()
    
    def init_machine(self):
        if self.geometry is None:
            return
        
        for i in range(len(self.geometry) - 1):
            pygame.draw.line(self.screen, self.geometry[i][0], self.geometry[i][1], self.geometry[i+1][1], 5)
            pygame.draw.circle(self.screen, GREEN,  self.geometry[i][1], 4)
        pygame.draw.circle(self.screen, GREEN, self.geometry[-1][1], 5)
        
        original_lengths = [
            distance(self.geometry[i][1], self.geometry[i+1][1]) for i in range(len(self.geometry) - 1)
        ]
        
        for i in range(len(self.geometry) - 1):
            cx, cy = self.geometry[i][1]
            angle = radians(self.angles[i])
            new_x = cx + original_lengths[i] * cos(angle)
            new_y = cy + original_lengths[i] * sin(angle)
            self.geometry[i+1][1] = [new_x, new_y]
        
        pygame.display.flip()
    
    def train_model(self):
        input_data = torch.tensor([self.target[0], self.target[1], self.geometry[-1][1][0], self.geometry[-1][1][1], self.angles[0], self.angles[1]], dtype=torch.float32)
        predicted_values = self.model(input_data)
        loss = self.criterion(predicted_values, torch.tensor([-self.geometry[-1][1][0], -self.geometry[-1][1][1], predicted_values[-4], predicted_values[-3], predicted_values[-2], predicted_values[-1]], dtype=torch.float32))
        print(loss, self.target[0], self.target[1],self.geometry[-1][1][0], self.geometry[-1][1][1])
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.angles[0] = predicted_values.detach().numpy()[-2]
        self.angles[1] = predicted_values.detach().numpy()[-1]
        
        print(self.angles)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        FPS = 60
        
        while running: 
            clock.tick(FPS)
            # print(self.angles)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False
            
            self.train_model()  # Train the model to predict angles
            
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.angles[0] += 0.5
            if keys[pygame.K_RIGHT]:
                self.angles[0] -= 0.5
            if keys[pygame.K_UP]:
                self.angles[1] += 0.5
            if keys[pygame.K_DOWN]:
                self.angles[1] -= 0.5
            
            self.screen.fill(WHITE)
            self.init_target()
            self.init_machine()
            # append_file(
            #     f"target-{self.target}-def-mach-config.csv",
            #     ["X0","Y0","X1","Y1","XF","YF","Angle0", "Angle1", "TargetX", "TargetY"],
            #     [self.geometry[0][1][0], self.geometry[0][1][1], self.geometry[1][1][0], self.geometry[1][1][1], self.geometry[2][1][0], self.geometry[2][1][1], self.angles[0], self.angles[1], self.target[0], self.target[1]]
            # )
            pygame.display.update()
        
        pygame.quit()
        
    def set_target(self, point):
        self.target = point
        
    def set_machine(self, geometry):
        self.geometry = geometry
        
if __name__ == "__main__":
    mach_config = [
        [RED, [300, 400]],
        [RED, [300, 300]],
        [RED, [300, 200]],
    ]
    env = Playground()
    env.set_target(point=(200, 200))
    env.set_machine(mach_config)
    env.run()
