
import math
from Settings import *
import os, sys, pygame
from PIL import Image
import numpy as np


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
CHARACTER_FOLDER = "Assets\Characters"

class Player(pygame.sprite.Sprite):
    def __init__(self, character, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = pygame.display.get_surface()
        
        # paramaters
        self.speed = 1
        self.jumpForce = -5
        self.dash_distance = 50
        self.gravity = 0.2
        self.collision_tolorance = 2
        self.direction = pygame.math.Vector2(0, 0)

        # booleans
        self.flipped = False
        self.jumped = False
        self.on_ground = False

        self.character = character
        self.animations_names = self.character.animations_folders
        self.selected_folder = self.animations_names[0]
        self.animation_index = 0
        self.current_animation = self.character.animations[self.selected_folder]["frames"][0]
        self.frames_path = os.path.join(ROOT, CHARACTER_FOLDER, self.character.character_name)
        
        self.image = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, "cropped", self.current_animation))
        old_rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (old_rect.w * 2, old_rect.h * 2))
        self.normal_image = self.image
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * SCALE_SIZE, y * SCALE_SIZE

    def repetitive_bullshit(self):
        old_rect = self.rect.copy()
        self.image = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, "cropped", self.current_animation[int(self.animation_index)]))
        self.image = pygame.transform.scale(self.image, (old_rect.width, old_rect.height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = old_rect.x, old_rect.y
        self.normal_image = self.image
        self.flipped_image = pygame.transform.flip(self.image, True, False)
    
    def input(self, collision_sprites):
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_LEFT]:
            self.direction.x = -1
            self.selected_folder = self.animations_names[1]
            self.current_animation = self.character.animations[self.selected_folder]["frames"]
            self.flipped = True
        elif keys_pressed[pygame.K_RIGHT]:
            self.direction.x = +1
            self.selected_folder = self.animations_names[1]
            self.current_animation = self.character.animations[self.selected_folder]["frames"]
            self.flipped = False
        else:
            self.direction.x = 0
            self.selected_folder = self.animations_names[0]
            self.current_animation = self.character.animations[self.selected_folder]["frames"]

        if keys_pressed[pygame.K_SPACE]:
            if self.jumped == False:
                self.jump(collision_sprites)

    def animate(self):
        self.animation_index += 0.15
        if self.animation_index >= len(self.character.animations[self.selected_folder]["frames"]):
            self.animation_index = 0
        
        self.repetitive_bullshit()

        if self.flipped:
            self.image = self.flipped_image
        else:
            self.image = self.normal_image
  
    def horizontal_vertical_collision(self, collision_sprites):
        self.apply_gravity()
        
        for sprite in collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumped = False
                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
        

        for sprite in collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    print(self.rect, sprite.rect, self.rect.left, sprite.rect.right)
                elif self.direction.x > 0:
                    self.rect.right = sprite.rect.left



    def jump(self, collision_sprites):
        self.fixed_collision_point[2] = 0
        self.direction.y = self.jumpForce
        self.jumped = True
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    # def update(self, collision_sprites):
    #     if self.fixed_collision_point[2] == 0:
    #         self.direction.y += self.gravity
    #         self.rect.y += self.direction.y
    #     else:
    #         self.rect.y = self.fixed_collision_point[2]
    
    def update(self, collision_sprites):
        self.rect.x += self.direction.x * self.speed
        self.input(collision_sprites)
        self.animate()
        self.horizontal_vertical_collision(collision_sprites)
        
    # def draw(self, screen):
    #     screen.blit(self.image, self.hitbox)

