
from Settings import *
import os, sys, pygame


class EXIT_RECT(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x, self.y, self.width, self.height = x, y, width, height
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.action = False
        self.enabled = False
    
    def update(self, player):
        if self.rect.colliderect(player.rect) and not self.action:
            self.action = player.trigger_floating_text("[NEXT ROOM]", self.rect.x + self.rect.w / 3, self.rect.y)
            if self.action:
                print("Passing through")
                self.action = False
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Item(pygame.sprite.Sprite):
    def __init__(self, width, height, animate, scale, side=None, x=0, y=0, scalex=2, scaley=2):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.animations = {}
        self.animation_names = []
        self.animation_index = 0
        self.animate = animate
        self.scale = scale
        self.side = side
        self.scalex, self.scaley = scalex, scaley
        self.disappear, self.hide_image = False, False
        self.x, self.y, self.width, self.height = x + (ROOM_OFFSET_X * SCALE_SIZE), y + (ROOM_OFFSET_Y * SCALE_SIZE), width, height
        if self.side:
            self.x = self.x + (( - 1 if self.side == "Right" else 1) * (SCALE_SIZE - self.width))
        self.rect = pygame.Rect(self.x, self.y + (SCALE_SIZE - self.height), self.width, self.height)
    
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
        self.status_path = os.path.join(self.path, self.status)
        self.old_rect = self.rect.copy()
        working_path = os.path.join(self.status_path, self.working_animation[int(self.animation_index)])
        self.image = pygame.image.load(working_path)
        self.rect.w, self.rect.h = self.image.get_rect().w, self.image.get_rect().h
        if self.scale:
            self.image = pygame.transform.scale(self.image, (self.rect.w * self.scalex, self.rect.h * self.scaley))
            self.rect = pygame.Rect(self.old_rect.x, self.old_rect.y, self.image.get_rect().w, self.image.get_rect().h)
        
    def play_animation(self):
        if self.animate:
            self.animation_index += 0.12
            if self.animation_index >= len(self.working_animation):
                self.animation_index = 0
            
            self.get_frame()

    def draw(self):
        self.play_animation()
        if not self.hide_image:
            self.display_surface.blit(self.image, self.rect)
        # pygame.draw.rect(self.display_surface, (255, 255, 255), self.rect, 1)

    def update(self, world_shift_x, world_shift_y):
        self.rect.x += world_shift_x
        self.rect.y += world_shift_y

    def shift(self, world_shift_x, world_shift_y):
        self.rect.x += world_shift_x
        self.rect.y += world_shift_y
        
    def set_position(self, x, y):
        self.rect.x, self.rect.y = x, y
    
    def set_status(self, status):
        self.status = status

    def delete(self, items):
        items.remove(self)
        
class GUI_ITEM(pygame.sprite.Sprite):
    def __init__(self, x, y, image, font=None, text=None):
        super().__init__()
        self.x, self.y = x, y
        self.font = font
        self.image = image
        self.text = text
        if font:
            self.image = self.font.render(str(text), False, (255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
    
    def set_text(self, text):
        self.image = self.font.render(str(text), False, (255, 255, 255))
    
    def update(self, offset_x, offset_y, player):
        self.x += offset_x
        self.x += offset_y
        
class GUI_ITEM_BAR(pygame.sprite.Sprite):
    def __init__(self, x, y, image, bar_type, player):
        super().__init__()
        self.x, self.y = x, y
        self.image = image
        self.player = player
        self.bar_type = bar_type
        self.bar_max = 3.24 if bar_type == "Mana" else 4.8
        self.max = player.max_mana if bar_type == "Mana" else player.max_health
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
    
    def update(self):
        self.bar_current = self.player.mana if self.bar_type == "Mana" else self.player.health
        if self.bar_current < self.max:
            if self.bar_type == "Mana": 
                self.player.mana += 0.25
            else:
                self.player.health += 0.8
            new_width = (self.bar_current * (32 * self.bar_max)) / self.max
            self.image = pygame.transform.scale(self.image, (new_width, 4))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            if self.bar_type == "Mana": 
                self.player.mana = self.max
            else:
                self.player.health = self.max        