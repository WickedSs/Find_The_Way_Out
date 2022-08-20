
from Settings import *
import os, sys, pygame


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
CHARACTER_FOLDER = "Assets\Characters"

class Player(pygame.sprite.Sprite):
    def __init__(self, character, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.animations_names = self.character.animations_folders
        self.selected_folder = self.animations_names[0]
        self.animation_index = 0
        self.frame = self.character.animations[self.selected_folder]["frames"][self.animation_index]
        self.frames_path = os.path.join(ROOT, CHARACTER_FOLDER, self.character.character_name)
        self.image = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, self.frame))
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(x, y)
        self.rect.x, self.rect.y = self.position.x * TILE_SIZE, self.position.y * TILE_SIZE
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.jumpForce = 5
        self.dash_distance = 10
        self.gravity = 5
    
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
        elif keys[pygame.K_RIGHT]:
            self.direction.x += 1
        else:
            self.direction.x = 0
        
    def animate(self):
        return
    
    def move(self, dt):
        self.position += self.direction * self.speed * dt
        self.rect.x, self.rect.y = self.position.x, self.position.y
        current_animation = self.character.animations[self.selected_folder]["frames"]
        self.frame = self.character.animations[self.selected_folder]["frames"][self.selecte]
        self.image = pygame.image.load(os.path.join(self.frames_path, self.selected_folder, self.frame))
            
        # collide = pygame.sprite.spritecollide(self, tiles, False)
        # if not collide:
        #     self.rect.y += self.gravity
        
    def update(self, dt):
        self.input()
        self.move(dt)


