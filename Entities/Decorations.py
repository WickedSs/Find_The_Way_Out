import os, sys, pygame, random, uuid, operator
from Entities.Item import Item
from Settings import *


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
        self.next_destination, self.destination_door, self.destination_room = None, None, None
        self.shift_distance_x, self.shift_distance_y = 0, 0
        self.open, self.action, self.played, self.shift = False, False, 0, False
        self.path = os.path.join(DECORATIONS_FOLDER, self.asset_name)
        self.multiple_animations()
        self.working_animation = self.animations[self.status]
        self.get_frame()

    def set_room_coords(self, room, door):
        self.room_coords = room
        self.door_coords = door

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
                # player.overlay.dim_screen_counter = 0
                # player.overlay.dim_screen_bool = status
                player.hide_player = True
                self.open = self.action = player.E_Action = False
                self.played = 1
                self.delay = pygame.time.get_ticks()
                if self.destination:
                    self.next_destination = random.choice(self.destination)
                    self.destination_room = self.next_destination.room_coords
                    self.destination_door = self.next_destination.door_coords
                    print("Old_position:", player.rect)
                    player.rect.x, player.rect.y = (self.destination_door[0] + ROOM_OFFSET_X) * SCALE_SIZE, (self.destination_door[1] + ROOM_OFFSET_Y) * SCALE_SIZE
                    if self.next_destination.rect.x - self.rect.x > 0:
                        self.offset_x = -self.destination_room[0]
                        self.offset_y = -self.destination_room[1]
                    else:
                        self.offset_x = self.destination_room[0]
                        self.offset_y = self.destination_room[1]
                    
                    sign_x = self.offset_x / -self.offset_x if self.offset_x != 0 else 0
                    sign_y = self.offset_y / -self.offset_y if self.offset_y != 0 else 0
                    player.level.camera.shift_to = self.destination_room
                    player.level.camera.set_increment((sign_x, sign_y))
                    player.level.camera.is_shifting = True
                    self.open = False
                    
        
        if self.delay:
            if (pygame.time.get_ticks() - self.delay) / 1000 >= 2:
                self.status = "Closing"
                status = self.play_animation_once()
                if status:
                    player.disable_movement = False
                    player.overlay.dim_screen_bool = False
                    player.overlay.trigger_fade_in = False
                    player.hide_player = False
                    print("New_position:", player.rect)
                    self.delay = None
                    self.played = 0
        
        if self.shift:
            if self.shift_distance_x != self.offset_x and self.shift_distance_y != self.offset_y:
                self.shift_distance_x += self.offset_x / 10 * 0.01
                self.shift_distance_y += self.offset_y / 10 * 0.01
            else:
                self.shift_distance_x = 0
                self.shift_distance_y = 0
            
                      
        # if self.destination_door:
        #     pygame.draw.rect(self.display_surface, (0, 255, 0), ((self.destination_door[0] + ROOM_OFFSET_X) * 64, (self.destination_door[1] + ROOM_OFFSET_Y) * 64, 64, 64), 1)
        #     pygame.draw.rect(self.display_surface, (0, 0, 255), player.rect, 1)
        
                
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