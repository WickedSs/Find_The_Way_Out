
from tkinter.tix import Tree
from Settings import *
import os, sys, pygame


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
CHARACTER_FOLDER = "Assets\Characters"

class Player(pygame.sprite.Sprite):
    def __init__(self, character, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.position = pygame.math.Vector2((x, y))
        self.direction = pygame.math.Vector2()
        self.animations_names = self.character.animations_folders
        self.selected_folder = self.animations_names[0]
        self.animation_index = 0
        self.current_animation = self.character.animations[self.selected_folder]["frames"]
        self.frames_path = os.path.join(ROOT, CHARACTER_FOLDER, self.character.character_name)
        
        self.image = self.scale_frame()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position.x * SCALE_SIZE, self.position.y * SCALE_SIZE

        self.speed = 0.05
        self.jumpForce = 5
        self.dash_distance = 50
        self.gravity = 50
        self.flipped = False
    
    def scale_frame(self):
        self.current_frame = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, self.current_animation[int(self.animation_index)]))
        self.frame_rect = self.current_frame.get_rect()
        image = pygame.Surface((self.frame_rect.width, self.frame_rect.height)).convert_alpha()
        image.set_colorkey((0, 0, 0))
        image.blit(self.current_frame, self.frame_rect)
        scaled_surface = pygame.transform.scale(image, (self.frame_rect.w * 2, self.frame_rect.h * 2)).convert_alpha()
        scaled_surface.set_colorkey((0, 0, 0))
        self.flipped_image = pygame.transform.flip(scaled_surface, True, False)
        self.normal_image = scaled_surface
        self.mask = pygame.mask.from_surface(scaled_surface)
        return scaled_surface
    
    def input(self, dt, collision_sprites):
        keys = pygame.key.get_pressed()
        
        for sprite in collision_sprites.sprites():
            sprite_mask = pygame.mask.from_surface(sprite.image)
            if sprite_mask.overlap(self.mask, (0, 0)):
                print(sprite.rect)

        if keys[pygame.K_UP]:
            self.direction.y -= 1
        elif keys[pygame.K_DOWN]:
            self.direction.y += 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_LEFT]:
            self.direction.x -= 1
            self.selected_folder = self.animations_names[1]
            self.current_animation = self.character.animations[self.selected_folder]["frames"]
            self.flipped = True
        elif keys[pygame.K_RIGHT]:
            self.direction.x += 1
            self.selected_folder = self.animations_names[1]
            self.current_animation = self.character.animations[self.selected_folder]["frames"]
            self.flipped = False
        else:
            self.direction.x = 0
            self.selected_folder = self.animations_names[0]
            self.current_animation = self.character.animations[self.selected_folder]["frames"]

        if keys[pygame.K_SPACE]:
            self.direction.y -= self.jumpForce

    def animate(self, dt):
        self.animation_index += 10 * dt
        if self.animation_index >= len(self.character.animations[self.selected_folder]["frames"]):
            self.animation_index = 0
        self.image = self.scale_frame()

        # flip player in which direction he is facing
        if self.flipped:
            self.image = self.flipped_image
        else:
            self.image = self.normal_image
        # self.frame = self.character.animations[self.selected_folder]["frames"][int(self.animation_index)]
        # self.image = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, self.frame))
        # self.image = pygame.transform.scale(self.image, (SCALE_SIZE, SCALE_SIZE))
  
    def move(self, dt):
        self.position += self.direction * self.speed * dt
        self.rect.x, self.rect.y = self.position.x * SCALE_SIZE, self.position.y * SCALE_SIZE
        # current_animation = self.character.animations[self.selected_folder]["frames"]
        
            
        # collide = pygame.sprite.spritecollide(self, tiles, False)
        # if not collide:
        #     self.rect.y += self.gravity
        
    def update(self, dt, collsion_sprites):
        self.input(dt, collsion_sprites)
        self.move(dt)
        self.animate(dt)


