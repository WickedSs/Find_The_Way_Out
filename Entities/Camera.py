
from pickle import TRUE
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame, sys, os, random, operator



class Camera:
    def __init__(self, level):
        self.level = level
        self.offset_x, self.offset_y = 128, 128
        self.rect = pygame.Rect(self.offset_x, self.offset_y, SCREEN_WIDTH - self.offset_x*2, SCREEN_HEIGHT - self.offset_y*2 - 56)
        self.is_shifting, self.shift_to, self.shift_ratio = False, None, 0.01
        self.current_position_x, self.current_position_y = (0, 0)
        self.increment_values, self.increment = (64, 64), (0, 0)
        self.horizontal, self.vertical = False, False
    
    def set_increment(self, sign):
        self.increment = tuple(map(operator.mul, self.increment_values, sign))
        self.shift_to = tuple(map(operator.mul, self.shift_to, sign))
        self.horizontal = True

    def shift_world(self):
        print("Shift Status:", self.horizontal, self.vertical, self.current_position_x, self.current_position_y, self.shift_to, self.increment)
        if self.horizontal and self.shift_to[0] != 0:
            if self.current_position_x != self.shift_to[0]:
                self.current_position_x += self.increment[0]
            else:
                self.horizontal = False
                self.vertical = True
        else:
            self.vertical = True
            self.horizontal = False
        
        if self.vertical and self.shift_to[1] != 0:  
            if self.current_position_y != self.shift_to[1]:
                self.current_position_y += self.increment[1]
            else:
                self.vertical = self.horizontal = False
        
        if not self.horizontal and not self.vertical:
            self.is_shifting = False
            self.shift_to = None
            self.increment = (0, 0)
        
    def shift_to_place(self, pos):
        for sprite in self.level.sprites_group.sprites():
            sprite.set_position(pos[0], pos[1])

    def update(self):
        if self.is_shifting:
            self.shift_world()
            self.values = (self.increment[0] if self.horizontal else 0, self.increment[1] if self.vertical else 0)
            self.level.sprites_group.update(self.values[0], self.values[1])
            self.level.infinite_group.update(self.values[0], self.values[1])
            self.level.single_group.update(self.values[0], self.values[1])
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)