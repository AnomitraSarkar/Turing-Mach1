import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 50
WATER_COLOR = (0,0,255)
MAX_RIPPLE_RADIUS = 150

def draw_ripples(surfaced, ripples, time_passed):
    for ripple in ripples:
        ripple["radius"] += int(time_passed * 100)
        if ripple["radius"] < MAX_RIPPLE_RADIUS:
            alpha = int(255 - (ripple["radius"]/MAX_RIPPLE_RADIUS)*255)
            ripple_color = (0, 160, 255, alpha)
            pygame.draw.circle(surfaced, ripple_color, ripple["center"], ripple["radius"])
            
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
  
    water_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
    ripples = []
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                ripples.append({"center": event.pos, "radius": 0})
        time_passed = min(clock.tick(FPS)/1000.0,0.1)
        draw_ripples(water_surface, ripples, time_passed)
        
        screen.fill(WATER_COLOR)
        screen.blit(water_surface, (0, 0))
        pygame.display.flip()
        
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()