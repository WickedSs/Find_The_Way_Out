
from pickle import TRUE
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame, sys, os, random, operator



class Camera:
    def __init__(self, level):
        self.level = level
        self.offset_x, self.offset_y = 64, 64
        self.rect = pygame.Rect(self.offset_x, self.offset_y, SCREEN_WIDTH - self.offset_x*2, SCREEN_HEIGHT - self.offset_y*2)
        print(self.rect)
        self.is_shifting, self.current_direction = False, "Right"
        self.current_position, self.shift_to = (0, 0), (0, 0)
        self.increment_values, self.increment = (64, 64), (0, 0)
        self.horizontal, self.vertical = False, False
    
    def get_increment_direction(self, direction):
        if direction == "left":
            self.shift_to = tuple(map(operator.add, self.shift_to, (SCREEN_WIDTH, 0)))
            self.increment = tuple(map(operator.mul, self.increment_values, (1, 0)))
            self.horizontal = True
        elif direction == "right":
            self.shift_to = tuple(map(operator.sub, self.shift_to, (SCREEN_WIDTH, 0)))
            self.increment = tuple(map(operator.mul, self.increment_values, (-1, 0)))
            self.horizontal = True
        elif direction == "up":
            self.shift_to = tuple(map(operator.add, self.shift_to, (0, SCREEN_HEIGHT)))
            self.increment = tuple(map(operator.mul, self.increment_values, (0, 1)))
            self.vertical = True
        elif direction == "down":
            self.shift_to = tuple(map(operator.sub, self.shift_to, (0, SCREEN_HEIGHT)))
            self.increment = tuple(map(operator.mul, self.increment_values, (0, -1)))
            self.vertical = True
        
        self.current_direction = direction

    def shift_world(self):
        self.current_position = tuple(map(operator.add, self.current_position, self.increment))
        self.can_move = True
        
        print("Current:", (self.current_position), "\tIncrement:", self.increment, "\tShift_to:", self.shift_to)
        
        

    def update(self):
        if self.is_shifting:
            self.shift_world()
            self.level.sprites_group.update(self.increment[0], self.increment[1])
            self.level.infinite_group.update(self.increment[0], self.increment[1])
            self.level.single_group.update(self.increment[0], self.increment[1])
            self.level.exit_group.update(self.increment[0], self.increment[1])
            if tuple(map(operator.sub, self.current_position, self.shift_to)) == (-64, 0):
                self.can_move = self.is_shifting = self.vertical = self.horizontal = False
                self.shift_to = None
                self.increment = (0, 0)
            
            
    def draw(self, screen):
        # pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
        return