
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
        self.current_frame = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, self.current_animation[self.animation_index]))
        # self.image = pygame.transform.scale(self.current_frame, (SCALE_SIZE, SCALE_SIZE))
        self.scale_sprite()
        self.rect = self.image.get_rect()
        print(self.rect)
        self.rect.x, self.rect.y = self.position.x * SCALE_SIZE, self.position.y * SCALE_SIZE
        
        self.speed = 3
        self.jumpForce = 5
        self.dash_distance = 10
        self.gravity = 5
    
    def scale_sprite(self):
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(self.current_frame, (0, 0), (self.position.x * TILE_SIZE, self.position.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return self.image
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y -= 1
        elif keys[pygame.K_DOWN]:
            self.direction.y += 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_LEFT]:
            self.direction.x -= 1
            self.selected_folder = self.animations_names[1]
            self.image = pygame.transform.flip(self.image, True, False)
        elif keys[pygame.K_RIGHT]:
            self.direction.x += 1
            self.image = pygame.transform.flip(self.image, True, False)
            self.selected_folder = self.animations_names[1]
        else:
            self.direction.x = 0
            self.selected_folder = self.animations_names[0]
        
    def animate(self, dt):
        self.animation_index += 7 * dt
        if self.animation_index >= len(self.character.animations[self.selected_folder]["frames"]):
            self.animation_index = 0
        self.frame = self.character.animations[self.selected_folder]["frames"][int(self.animation_index)]
        self.image = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, self.frame))
        self.image = pygame.transform.scale(self.image, (SCALE_SIZE, SCALE_SIZE))
  
    def move(self, dt):
        self.position += self.direction * self.speed * dt
        self.rect.x, self.rect.y = self.position.x * SCALE_SIZE, self.position.y * SCALE_SIZE
        # current_animation = self.character.animations[self.selected_folder]["frames"]
        
            
        # collide = pygame.sprite.spritecollide(self, tiles, False)
        # if not collide:
        #     self.rect.y += self.gravity
        
    def update(self, dt):
        self.input()
        self.move(dt)
        # self.animate(dt)


