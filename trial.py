import pygame

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pygame Text Example")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load a font (None = default font, size = 36)
font = pygame.font.Font(None, 36)

# Render text
count = 0

running = True
while running:
    count += 1
    text = font.render(f"Hello, Pygame! {count}", True, WHITE)  # True = Anti-aliasing
    text_rect = text.get_rect(center=(300, 200))  # Position at center
    screen.fill(BLACK)  # Clear screen
    screen.blit(text, text_rect)  # Draw text
    pygame.display.flip()  # Update display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
