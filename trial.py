import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Lines")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Nodes with colors and coordinates
nodes = [
    [[255, 0, 0], [300, 400]],
    [[255, 0, 0], [300, 300]],
    [[255, 0, 0], [300, 200]],
]

# Rotation settings
angles = [0, 45, 0]  # Individual rotation angles for each node
rotation_speed = 5  # Degrees per key press
original_lengths = [
    math.dist(nodes[i][1], nodes[i + 1][1]) for i in range(len(nodes) - 1)
]  # Store original distances

def rotate_point(px, py, angle, cx, cy):
    """Rotate a point around (cx, cy) by the given angle."""
    radians = math.radians(angle)
    cos_a = math.cos(radians)
    sin_a = math.sin(radians)
    # new_x = cos_a * (px - cx) - sin_a * (py - cy) + cx
    # new_y = sin_a * (px - cx) + cos_a * (py - cy) + cy
    new_x = cos_a * (px - cx) + cx
    new_y = sin_a * (px - cx) + cy
    return int(new_x), int(new_y)

running = True
while running:
    screen.fill(WHITE)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angles = [angles[a] + rotation_speed  if a%2!=0 else angles[a] for a in range(len(angles))]  # Rotate all counterclockwise
    if keys[pygame.K_RIGHT]:
        angles = [a - rotation_speed for a in angles]  # Rotate all clockwise

    # Rotate each node while maintaining original distances
    rotated_nodes = [nodes[0][1]]  # First node remains the same
    for i in range(1, len(nodes)):
        _, (x, y) = nodes[i]
        cx, cy = rotated_nodes[i - 1]  # Use previous node as center
        angle = angles[i]
        new_x, new_y = rotate_point(cx + original_lengths[i - 1], cy, angle, cx, cy)
        rotated_nodes.append((new_x, new_y))
    
    # Draw rotated lines
    for i in range(len(rotated_nodes) - 1):
        pygame.draw.line(screen, RED, rotated_nodes[i], rotated_nodes[i + 1], 5)
    
    pygame.display.flip()
    pygame.time.delay(30)  # Smooth animation

pygame.quit()
