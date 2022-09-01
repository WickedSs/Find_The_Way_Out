
from pickle import TRUE
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame, sys, os, random, operator



class Camera:
    def __init__(self, level):
        self.level = level
        self.offset_x, self.offset_y = 64, 64
        self.rect = pygame.Rect(self.offset_x, self.offset_y, SCREEN_WIDTH - self.offset_x*2, SCREEN_HEIGHT - self.offset_y*2)
        print(self.rect)
        self.is_shifting, self.shift_to, self.shift_ratio = False, None, 0.01
        self.current_position_x, self.current_position_y = (0, 0)
        self.increment_values, self.increment = (64, 64), (0, 0)
        self.horizontal, self.vertical = False, False
    
    def set_increment(self, sign, shift_to):
        self.sign = (-1, -1) if sign == (0, 0) else sign
        self.increment = tuple(map(operator.mul, self.increment_values, sign))
        self.shift_to = tuple(map(operator.add, (self.current_position_x, self.current_position_y), shift_to))
        
        if self.current_position_x != self.shift_to[0] and self.shift_to[0] != 0:
            self.horizontal = True
            self.vertical = False
        elif self.current_position_y != self.shift_to[1] and self.shift_to[1] != 0 and not self.horizontal:
            self.horizontal = False
            self.vertical = True
        
        print("Current:", (self.current_position_x, self.current_position_y), "\tIncrement:", self.increment,"\tShift_to:", self.shift_to, self.horizontal, self.vertical)
        

    def shift_world(self):
        if self.horizontal:
            # print("dest:", self.shift_to, "Current:", (self.current_position_x, self.current_position_y), "Increment:", self.increment, "Horizontal")
            if self.current_position_x != self.shift_to[0]:
                self.current_position_x += self.increment[0]
                self.can_move = True
            else:
                self.horizontal = False
                if self.shift_to[1] != 0:
                    self.vertical = True
                    self.shift_to = (self.shift_to[0], self.shift_to[1])       
                
        elif self.vertical:  
            # print("dest:", self.shift_to, "Current:", (self.current_position_x, self.current_position_y), "Increment:", self.increment, "Vertical")
            if self.current_position_y != self.shift_to[1] - (64 * self.sign[1]):
                self.current_position_y += self.increment[1]
                self.can_move = True
            else:
                self.can_move = self.is_shifting = self.vertical = self.horizontal = False
                self.shift_to = None
                self.increment = (0, 0)
                
                

    def update(self):
        if self.is_shifting:
            self.shift_world()
            if self.can_move:
                self.values = (self.increment[0] if self.horizontal else 0, self.increment[1] if self.vertical else 0)
                self.level.sprites_group.update(self.values[0], self.values[1])
                self.level.infinite_group.update(self.values[0], self.values[1])
                self.level.single_group.update(self.values[0], self.values[1])
                self.level.exit_group.update(self.values[0], self.values[1])
            
            
    def draw(self, screen):
        # pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
        return