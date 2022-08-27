import os, sys, pygame
import random
from Entities.Item import *
from Settings import *
from Entities.Particles import *

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
ITEMS_FOLDER = "Assets\Items"





class Big_Map(Item):
    def __init__(self, width, height, animate, scale, x, y):
        super().__init__(width, height, animate, scale, x, y, 1, 1)
        self.display_surface = pygame.display.get_surface()
        self.asset_name = "Big_Map"
        self.animation_type = "Multiple"
        self.status = "Idle"
        self.path = os.path.join(ITEMS_FOLDER, self.asset_name)
        self.status_path = os.path.join(self.path, self.status)
        self.multiple_animations()
        self.working_animation = self.animations[self.status]
        self.out_particle = Big_Map_particle("Out", 19, 19)
        self.get_frame()
        
    def on_pickup(self, player):
        if player.rect.colliderect(self.rect) and not self.hide_image:
            self.out_particle.set_position(self.rect.x, self.rect.y)
            self.hide_image = True

        if self.hide_image:
            self.disappear = self.out_particle.play_animation_once()
    
    def play_animation_once(self, player):
        self.animation_index += 0.12
        if self.animation_index >= len(self.working_animation):
            self.animation_index = 0
            self.player_effect(player)
            return True
        
        self.get_frame()
        self.rect.y -= int(self.animation_index)
        self.display_surface.blit(self.image, self.rect)
        return False
    
    def player_effect(self, player):
        player.collected_maps += 1
        return


class Chest(Item):
    def __init__(self, width, height, animate, scale, x, y):
        super().__init__(width, height, animate, scale, x, y)
        self.asset_name = "Chest"
        self.animation_type = "Multiple"
        self.status = "Idle"
        self.open, self.item = False, False
        self.path = os.path.join(ITEMS_FOLDER, self.asset_name)
        self.multiple_animations()
        self.working_animation = self.animations[self.status]
        self.possible_loot = [Big_Map(30, 31, True, True, 1 * SCALE_SIZE, 4 * SCALE_SIZE)]
        self.get_frame()
        # self.big_map = Big_Map(30, 31, True, 1 * SCALE_SIZE, 4 * SCALE_SIZE)
        
    def on_collision(self, player, items_list):
        if player.rect.colliderect(self.rect) and not self.open:
            action = player.trigger_floating_text("[E]", self.rect.x + self.rect.w / 4, self.rect.y - (self.rect.h / 2))
            if action:
                self.status = "Unlocked"
                self.working_animation = self.animations[self.status]
                self.open = True
        
        # print(self.item, self.open)
        if self.open and not self.item:
            self.item = self.play_animation_once()
            self.open = False
        
        if self.item:
            self.pick_item(player, items_list)
            
    def play_animation_once(self):
        self.animation_index += 0.12
        if self.animation_index >= len(self.working_animation):
            self.animation_index = 0
            return True
        
        self.get_frame()
        self.display_surface.blit(self.image, self.rect)
        return False
        
    def pick_item(self, player, items_list):
        random_item = random.choice(self.possible_loot)
        random_item.rect.x, random_item.rect.y = self.rect.x + (self.rect.w / 4), self.rect.y - (self.rect.h / 3)
        status = random_item.play_animation_once(player)
        if status:
            self.player_effect(player)
            self.open = False
            items_list.remove(self)
    
    def player_effect(self, player):
        return

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

