from math import ceil
from multiprocessing import current_process
from tkinter import Grid
from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string, operator
from Entities.Cell import Room
from Entities.Tile import *
from Settings import *
import xml.etree.ElementTree as ET
import json


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
LEVELS_FOLDER = "Assets/Levels"
SPRITES = []


PARTICLE_EFFECTS = {

}



class Level_CONFIG:
    def __init__(self, data):
        self.data = data
        self.load_json()
    
    def load_json(self):
        self.collide_layer = self.data["layers"][0]["data"]
        self.background_layer = self.data["layers"][1]["data"]
        self.tile_width, self.tile_height = self.data["tilewidth"], self.data["tileheight"]
        self.room_width, self.room_height = self.data["width"], self.data["height"]
    

class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    def __init__(self, overlay):
        global SPRITES
        self.overlay = overlay
        self.display_surface = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.level_sprite_sheet = None
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.layout_in_use = "First_Layout"
        self.levels, self.picked_level = [], 0
        self.world_shift = 0
        self.scroll_offset = [0, 0]
        self.DIM = 2
        self.infinite_list, self.single_list = [], []
        self.initialize()

    def initialize(self):
        self.sprites_group = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        self.infinite_group = pygame.sprite.Group()
        self.single_group = pygame.sprite.Group()
        self.initialize_grid()
        self.load_json_levels()
        self.initialize_sprite()
        self.generate_map()
    
    def scroll_X(self, player):
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if direction_x < 0 and not player.blocked:
            self.world_shift = PLAYER_SPEED
            player.speed = 0
        elif direction_x > 0 and not player.blocked:
            self.world_shift = -PLAYER_SPEED
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = PLAYER_SPEED

    def dash_scroll(self):
        self.world_shift = 150

    def get_sprite(self, x, y, sprite_sheet):
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((0,0,0))
        sprite.blit(sprite_sheet, (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
        return pygame.transform.scale(sprite, (SCALE_SIZE, SCALE_SIZE))

    def load_json_levels(self):
        folder = os.path.join(ROOT, LEVELS_FOLDER)
        for filename in os.listdir(folder):
            file = os.path.join(ROOT, LEVELS_FOLDER, filename)
            json_file = open('{}'.format(file))
            data = json.load(json_file)
            level = Level_CONFIG(data)
            self.levels.append(level)

    def initialize_sprite(self):
        for y in range(0, self.sprite_sheet_rect.height, TILE_SIZE):
            for x in range(0, self.sprite_sheet_rect.width, TILE_SIZE):
                image = self.get_sprite(x, y, self.sprite_sheet)
                SPRITES.append(image)

    def initialize_grid(self):
        self.grid = []
        for i in range(DIM * DIM):
            self.grid.append(Room(i, self.infinite_group, self.single_group, SPRITES, self.sprites_group, self.collision_group))
            
    def generate_map(self):
        if DIM > 1:
            for j in range(self.DIM):
                for i in range(self.DIM):
                    index = i + j * self.DIM
                    self.picked_level = random.choice(self.levels)
                    self.grid[index].set_level(self.picked_level, self.levels.index(self.picked_level), i, j)
        else:
            self.picked_level = random.choice(self.levels)
            self.grid[0].set_level(self.picked_level, self.levels.index(self.picked_level), 0, 0)
    
    def run(self, player):
        self.sprites_group.update(self.world_shift, 0)
        self.sprites_group.draw(self.display_surface)
        
        # print("Lengths: ", len(self.single_group.sprites()), len(self.infinite_group.sprites()))
        
        for item in self.infinite_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 255, 0), item.rect, 1)
            item.on_pickup(player)
            item.update(self.world_shift, 0)
            item.draw()
            if item.disappear:
                self.overlay.set_text_to_slide("Part of the map was found!")
                self.overlay.trigger_sliding_text = True
                item.player_effect(player)
                self.items.remove(item)
        
        for decoration in self.single_group.sprites():
            # pygame.draw.rect(self.display_surface, (0, 255, 0), decoration.rect, 1)
            decoration.on_collision(player, self.single_list)
            decoration.update(self.world_shift, 0)
            decoration.draw()
        
        
        self.scroll_X(player)
    