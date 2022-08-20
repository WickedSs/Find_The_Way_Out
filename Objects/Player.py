
from Settings import *
import os, sys, pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, character, x, y):
        self.character = character
        self.image = self.character.animations["Idle"][0]
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = self.x, self.y
        self.speed = 3
        self.jumpForce = 5
        self.dash_distance = 10
        self.gravity = 5

    def update(self, tiles):
        collide = pygame.sprite.spritecollide(self, tiles, False)
        if not collide:
            self.rect.y += self.gravity

