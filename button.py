import random
import time
import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, color_on, color_off, sound, x, y): # Add given properties as parameters
        pygame.sprite.Sprite.__init__(self)
        self.color_on = color_on
        self.color_off = color_off
        self.sound = sound
        self.image = pygame.Surface((230, 230))
        self.image.fill(self.color_off)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self, screen):
    # blit image here
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def selected(self, mouse_pos):
    # Check if button was selected. Pass in mouse_pos.
        return self.rect.collidepoint(mouse_pos)
        
    def update(self, screen):
    # Illuminate button by filling color here
    # blit the image here so it is visible to the player
    # Play sound
        self.image.fill(self.color_on)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.sound.play()
        pygame.display.update()
        pygame.time.wait(500)
        self.image.fill(self.color_off)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()