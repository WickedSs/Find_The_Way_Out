
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
        self.fixed_collision_point = [0, 0, 0, 0] # top, right, bottom, left
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
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.w * 2, self.rect.h * 2))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * SCALE_SIZE, y * SCALE_SIZE

        # self.up_hitbox = pygame.Rect(self.rect.x + (self.rect.width / 2) - 5, self.rect.y + croppedBox[0], 10, 10)
        # self.right_hitbox = pygame.Rect(self.rect.x + (croppedBox[3] * 2) - 2, self.rect.y + (self.rect.height / 2) - 5, 10, 10)
        # self.down_hitbox = pygame.Rect(self.rect.x + (self.rect.width / 2) - 5, self.rect.y + (croppedBox[1] * 2) - 2, 10, 10)
        # self.left_hitbox = pygame.Rect(self.rect.x + (croppedBox[2] * 2) - 5, self.rect.y + (self.rect.height / 2) - 5, 10, 10)

    # def trim_images(self, image):
    #     image_name = self.current_animation[int(self.animation_index)].split(".")[0]

    #     image_old = os.path.join(image, "cropped", image_name + ".png")
    #     image_loaded = Image.open(image_old)
    #     image_loaded.load()

    #     image_data = np.asarray(image_loaded)
    #     image_data_bw = image_data.max(axis=2)
    #     non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    #     non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
    #     cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
    #     return cropBox

    def scale_frame(self):
        image_path = os.path.join(self.frames_path, self.selected_folder)
        croppedBox = self.trim_images(image_path)
        normal_height, normal_width = croppedBox[1] - croppedBox[0], croppedBox[3] - croppedBox[2]
        scaled_height, scaled_width = normal_height * 2, normal_width * 2
        
        self.current_frame = pygame.image.load(os.path.join(image_path, self.current_animation[int(self.animation_index)])).convert_alpha()
        self.current_frame.set_colorkey((0, 0, 0))
        self.frame_rect = self.current_frame.get_rect()
        scaled_surface = pygame.transform.scale(self.current_frame, (self.frame_rect.w * 2, self.frame_rect.h * 2)).convert_alpha()
        self.flipped_image = pygame.transform.flip(scaled_surface, True, False)
        self.normal_image = scaled_surface
        return scaled_surface, (scaled_width + 2, scaled_height + 2), croppedBox
    
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
        self.animation_index += 10
        if self.animation_index >= len(self.character.animations[self.selected_folder]["frames"]):
            self.animation_index = 0
        
        self.image, dimensions, croppedBox = self.scale_frame()
        self.hitbox = pygame.Rect((croppedBox[2] * 2) + self.rect.x, (croppedBox[0] * 2) + self.rect.y, dimensions[0], dimensions[1])

        # flip player in which acceleration he is facing
        if self.flipped:
            self.image = self.flipped_image
        else:
            self.image = self.normal_image
        # self.frame = self.character.animations[self.selected_folder]["frames"][int(self.animation_index)]
        # self.image = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, self.frame))
        # self.image = pygame.transform.scale(self.image, (SCALE_SIZE, SCALE_SIZE))
  
    def move(self, collision_sprites):
        self.rect.x += self.direction.x * self.speed
<<<<<<< HEAD
        self.apply_gravity()

        # horizonatl collision
        for sprite in collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                self.rect.x = self.rect.x + abs(self.hitbox.x - self.rect.x)
            if sprite.rect.colliderect(self.rect):
                self.rect.x = self.rect.x - abs(self.hitbox.x - self.rect.x)
                
        
        for sprite in collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                self.rect.top = sprite.rect.bottom
            if sprite.rect.colliderect(self.rect):
                self.rect.bottom = sprite.rect.top
                self.direction.y = 0
=======
        self.hitbox.x += self.direction.x * self.speed
        self.apply_gravity()

        # horizonatl collision
        # for sprite in collision_sprites.sprites():
        #     self.fixed_collision_point_x = 0
        #     if sprite.rect.colliderect(self.hitbox):
        #         self.hitbox.left = sprite.rect.right
        #         # self.rect.x = self.rect.x - abs(sprite.rect.x - self.rect.x)
        #     if sprite.rect.colliderect(self.hitbox):
        #         self.hitbox.right = sprite.rect.left
        #         # self.rect.x = self.rect.x + abs(sprite.rect.x - self.rect.x)
                
        
        collided_with = pygame.sprite.spritecollide(self, collision_sprites, False)
        if collided_with:
            print("Falling: ", abs(self.hitbox.bottom - collided_with[0].rect.top), collided_with)
            if abs(self.hitbox.bottom - collided_with[0].rect.top) <= self.collision_tolorance:
                self.direction.y, self.jumped = 0, False
                self.fixed_collision_point[2] = self.rect.y
            elif abs(self.hitbox.top - collided_with[0].rect.bottom) <= self.collision_tolorance:
                self.fixed_collision_point[0] = self.rect.y
            else:
                self.fixed_collision_point[0], self.fixed_collision_point[2] = 0, 0
            #     self.rect.bottom = self.rect.bottom + abs(self.rect.bottom - self.hitbox.bottom)
            #     self.rect.top = sprite.rect.bottom
            # self.fixed_collision_point[2] = self.rect.y
>>>>>>> 1fa1d39f3d87b7ac27d0eb8b5022e2abf5ee8c4e


    def jump(self, collision_sprites):
        self.fixed_collision_point[2] = 0
        self.direction.y = self.jumpForce
        self.jumped = True
        
    def apply_gravity(self):
<<<<<<< HEAD
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def update(self, collision_sprites):
=======
        if self.fixed_collision_point[2] == 0:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y
            self.hitbox.y += self.direction.y
        else:
            self.rect.y = self.fixed_collision_point[2]
    
    def update(self, collision_sprites):
        # print(self.rect, self.direction, self.fixed_collision_point)
>>>>>>> 1fa1d39f3d87b7ac27d0eb8b5022e2abf5ee8c4e
        self.input(collision_sprites)
        self.move(collision_sprites)
        # self.animate()
        
    # def draw(self, screen):
    #     screen.blit(self.image, self.hitbox)

