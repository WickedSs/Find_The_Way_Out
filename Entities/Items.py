import os, sys, pygame
from Entities.Item import *
from Settings import *

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
ITEMS_FOLDER = "Assets\Items"





class Big_Map(Item):
    def __init__(self, x, y):
        self.display_surface = pygame.display.get_surface()
        self.asset_name = "Big_Map"
        self.animation_type = "Multiple"
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x + (30 / 2 ), self.y + (31 / 2 ), 0, 0)
        self.animations = {}
        self.animation_names = []
        self.animation_index = 0
        self.status = "Idle"
        self.path = os.path.join(ITEMS_FOLDER, self.asset_name)
        self.status_path = os.path.join(self.path, self.status)
        self.multiple_animations()
        self.working_animation = self.animations[self.status]
        
    def on_pickeup(self, player):
        if player.rect.colliderect(self.rect):
            return True

        return False


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

