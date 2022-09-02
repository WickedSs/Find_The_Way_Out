
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
            self.shift_to = tuple(map(operator.add, self.current_position, (SCREEN_WIDTH, 0)))
            self.increment = tuple(map(operator.mul, self.increment_values, (1, 0)))
            self.horizontal = True
        elif direction == "right":
            self.shift_to = tuple(map(operator.sub, self.current_position, (SCREEN_WIDTH, 0)))
            self.increment = tuple(map(operator.mul, self.increment_values, (-1, 0)))
            self.horizontal = True
        elif direction == "up":
            self.shift_to = tuple(map(operator.add, self.current_position, (0, SCREEN_HEIGHT)))
            self.increment = tuple(map(operator.mul, self.increment_values, (0, 1)))
            self.vertical = True
        elif direction == "down":
            self.shift_to = tuple(map(operator.sub, self.current_position, (0, SCREEN_HEIGHT)))
            self.increment = tuple(map(operator.mul, self.increment_values, (0, -1)))
            self.vertical = True
        
        self.is_shifting = True
        self.current_direction = direction

    def shift_world(self, player):
        if self.is_shifting:
            self.current_position = tuple(map(operator.add, self.current_position, self.increment))
            self.level.sprites_group.update(self.increment[0], self.increment[1])
            self.level.infinite_group.update(self.increment[0], self.increment[1])
            self.level.single_group.update(self.increment[0], self.increment[1])
            self.level.exit_group.update(self.increment[0], self.increment[1])
            if self.current_position == self.shift_to:
                self.is_shifting = False
                self.increment = (0, 0)
                if self.current_direction in ["right", "left"]:
                    player.rect.x = 96 if self.current_direction == "right" else (SCREEN_WIDTH - 160)
                else:
                    player.rect.y = 96 if self.current_direction == "up" else -96
                player.hide_player = False
        
        

    def update(self, player):
        self.shift_world(player)
            
            
            
    def draw(self, screen):
        # pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
        return