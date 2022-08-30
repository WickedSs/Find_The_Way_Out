
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame, sys, os, random, operator



class Camera:
    def __init__(self, level):
        self.level = level
        self.offset_x, self.offset_y = 128, 128
        self.rect = pygame.Rect(self.offset_x, self.offset_y, SCREEN_WIDTH - self.offset_x*2, SCREEN_HEIGHT - self.offset_y*2 - 56)
        self.is_shifting, self.shift_to, self.shift_ratio = False, None, 0.01
        self.current_position = (0, 0)
    
    def set_increment(self):
        self.increment = (self.shift_to[0]/15*self.shift_ratio, self.shift_to[1]/15*self.shift_ratio)
    
    def shift_world(self):
        print("Shift Sattus:", self.current_position, self.shift_to, self.increment)
        if self.current_position <= self.shift_to:
            self.current_position = tuple(map(operator.add, self.current_position, self.increment))
            self.level.sprites_group.update(self.current_position[0], self.current_position[1])
            self.level.infinite_group.update(self.current_position[0], self.current_position[1])
            self.level.single_group.update(self.current_position[0], self.current_position[1])
        else:
            self.is_shifting = False 
            self.shift_to = None
    
    def update(self):
        if self.is_shifting:
            self.shift_world()
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)