import pygame
from Settings import *



class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, position, image, index, collision=False):
        super().__init__()
        self.index = index
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.x, self.y, self.position = x, y, position
        self.collision = collision 
        self.rect = self.image.get_rect()
        self.rect.x = ((self.x + ROOM_OFFSET_X) * SCALE_SIZE) + self.position[0]
        self.rect.y = ((self.y + ROOM_OFFSET_Y) * SCALE_SIZE) + self.position[1]

    def set_colision(self, collision):
        self.collision = collision

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift

    def set_position(self, x_pos, y_pos):
        self.rect.x += x_pos
        self.rect.y += y_pos
    
