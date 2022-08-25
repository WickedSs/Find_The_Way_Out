
from Settings import *
import os, sys, pygame

class Item:
    
    def multiple_animations(self):
        for folder in os.listdir(self.path):
            self.animations[folder] = []
            for frame in os.listdir(os.path.join(self.path, folder)):
                self.animations[folder].append(frame)

    def single_animations(self):
        self.animations["frame"] = []
        for frame in os.listdir(self.path):
            self.animations["frame"].append(frame)

    def get_frame(self):
        self.old_rect = self.rect.copy()
        working_path = os.path.join(self.status_path, self.working_animation[int(self.animation_index)])
        self.image = pygame.image.load(working_path)
        self.rect.w, self.rect.h = self.image.get_rect().w, self.image.get_rect().h

    def play_animation(self):
        self.animation_index += 0.12
        if self.animation_index >= len(self.working_animation):
            self.animation_index = 0
        
        self.get_frame()

    def draw(self):
        self.play_animation()
        self.display_surface.blit(self.image, self.rect)
        # pygame.draw.rect(self.display_surface, (255, 255, 255), self.rect, 1)

    def update(self, world_shift_x, world_shift_y):
        self.rect.x += world_shift_x
        self.rect.y += world_shift_y
        
    def set_position(self, x, y):
        self.rect.x, self.rect.y = x * SCALE_SIZE, y * SCALE_SIZE
    
    def set_status(self, status):
        self.status = status