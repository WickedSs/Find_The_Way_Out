import os, sys, pygame, random, uuid
from Entities.Item import Item


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
DECORATIONS_FOLDER = "Assets\Decorations"



class Cannon:
    def __init__(self):
        pass


class Candle:
    def __init__(self):
        pass
    

class Chains:
    def __init__(self, x, y):
        pass

class Door(Item):
    def __init__(self, width, height, animate, scale, side, x, y):
        super().__init__(width, height, animate, scale, side, x, y)
        self.id = str(uuid.uuid4()).split("-")[0]
        self.asset_name = "Door"
        self.animation_type = "Multiple"
        self.animations = {}
        self.animation_index = 0
        self.status = "Opening"
        self.delay = None
        self.destinations = None
        self.next_destination = None
        self.open, self.action, self.played = False, False, 0
        self.path = os.path.join(DECORATIONS_FOLDER, self.asset_name)
        self.multiple_animations()
        self.working_animation = self.animations[self.status]
        self.get_frame()

    def set_destination(self, destination):
        self.destination = destination
        # print("Door: ", self.id, [filt.id for filt in self.destination])

    def on_collision(self, player, items_list, level):
        if player.rect.colliderect(self.rect) and not self.open and not self.action:
            self.action = player.trigger_floating_text("[E]", self.rect.x + self.rect.w / 3, self.rect.y)
            if self.action:
                self.working_animation = self.animations[self.status]
                self.open = True
            
        if self.open and self.action and self.played == 0:
            self.status = "Opening"
            status = self.play_animation_once()
            player.disable_movement = True
            if status:
                player.overlay.dim_screen_counter = 0
                player.overlay.dim_screen_bool = status
                self.open = self.action = player.E_Action = False
                self.played = 1
                self.delay = pygame.time.get_ticks()
                player.hide_player = True
                if self.destination:
                    self.next_destination = random.choice(self.destination)
                    next_position = (self.next_destination.rect.x, self.next_destination.rect.y)
                    player.rect.x, player.rect.y = next_position[0], next_position[1]
                    direction_x = self.next_destination.x - self.rect.x
                    direction_y = self.next_destination.y - self.rect.y
                    level.sprites_group.update(direction_x, direction_y)
                    level.infinite_group.update(direction_x, direction_y)
                    level.single_group.update(direction_x, direction_y)
        
        if self.delay:
            if (pygame.time.get_ticks() - self.delay) / 1000 >= 2:
                self.status = "Closing"
                status = self.play_animation_once()
                if status:
                    player.disable_movement = False
                    self.delay = None
                    self.played = 0
                    player.overlay.dim_screen_bool = False
                    player.overlay.trigger_fade_in = False
                    player.hide_player = False
                    print("New_position:", self.rect)
                    player.level.world_shift = 0
                    
                
    def play_animation_once(self):
        self.animation_index += 0.12
        if self.animation_index >= len(self.working_animation):
            self.animation_index = 0
            return True
        
        self.get_frame()
        self.display_surface.blit(self.image, self.rect)
        return False

class Window:
    def __init__(self):
        pass

    
class Barrel_UP:
    def __init__(self):
        pass


class Barrel_Down:
    def __init__(self):
        pass
    

class Bottle_UP_1:
    def __init__(self):
        pass
    

class Bottle_UP_2:
    def __init__(self):
        pass
    

class Bottle_Down_1:
    def __init__(self):
        pass
    

class Bottle_Down_2:
    def __init__(self):
        pass