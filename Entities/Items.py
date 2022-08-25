import os, sys
import pygame

from Settings import SCALE_SIZE

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
ITEMS_FOLDER = "Assets\Items"



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
        # self.old_rect = self.image.get_rect()
        # self.image = pygame.transform.scale(self.image, (self.old_rect.w * 2, self.old_rect.h * 2))
        self.rect.w, self.rect.h = self.image.get_rect().w, self.image.get_rect().h

    def play_animation(self):
        self.animation_index += 0.12
        if self.animation_index >= len(self.working_animation):
            self.animation_index = 0
        
        self.get_frame()

    def draw(self):
        self.play_animation()
        self.display_surface.blit(self.image, self.rect)

    def update(self, world_shift_x, world_shift_y):
        print(world_shift_x, world_shift_y, self.rect)
        self.rect.x += world_shift_x
        self.rect.y += world_shift_y

    def on_pickeup(self):
        return


class Big_Map(Item):
    def __init__(self, x, y):
        self.display_surface = pygame.display.get_surface()
        self.asset_name = "Big_Map"
        self.animation_type = "Multiple"
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x + (self.rect.w / 2 ), self.y + (self.rect.h / 2 ), 0, 0)
        self.animations = {}
        self.animation_names = []
        self.animation_index = 0
        self.status = "Idle"
        self.path = os.path.join(ITEMS_FOLDER, self.asset_name)
        self.status_path = os.path.join(self.path, self.status)
        self.multiple_animations()
        self.working_animation = self.animations[self.status]
        
    def set_status(self, status):
        self.status = status

    def set_position(self, x, y):
        self.rect.x, self.rect.y = x * SCALE_SIZE, y * SCALE_SIZE


class Blue_Diamond(Item):
    def __init__(self):
        self.asset_name = "Blue_Diamond"
        self.animation_type = "Single"
        self.animations = {}
        self.animation_names = []
        self.path = os.path.join(ITEMS_FOLDER, self.asset_name)
        self.single_animations()
        self.working_animation = self.animations["frame"]

class Blue_Potion(Item):
    def __init__(self):
        pass


class Gold_Coin(Item):
    def __init__(self):
        pass


class Silver_Coin(Item):
    def __init__(self):
        pass

    
class Golden_Skull(Item):
    def __init__(self):
        pass


class Green_Bottle(Item):
    def __init__(self):
        pass


class Green_Diamond(Item):
    def __init__(self):
        pass


class Red_Diamond(Item):
    def __init__(self):
        pass
    

class Red_Postion(Item):
    def __init__(self):
        pass

