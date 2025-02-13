keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.angles[0] += 0.5
            if keys[pygame.K_RIGHT]:
                self.angles[0] -= 0.5
            if keys[pygame.K_UP]:
                self.angles[1] += 0.5
            if keys[pygame.K_DOWN]:
                self.angles[1] -= 0.5