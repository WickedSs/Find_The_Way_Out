

from Settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame, sys, os, random



class Camera:
    def __init__(self):
        self.offset_x, self.offset_y = 128, 128
        self.rect = pygame.Rect(self.offset_x, self.offset_y, SCREEN_WIDTH - self.offset_x*2, SCREEN_HEIGHT - self.offset_y*2 - 56)
        
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)