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
GRID = []
VISITED = []
DIM = 8



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
    def __init__(self):
        global SPRITES
        self.display_surface = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.level_sprite_sheet = None
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.layout_in_use = "First_Layout"
        self.levels, self.picked_level = [], 0
        self.world_shift = 0
        self.scroll_offset = [0, 0]
        self.DIM = 2
        self.initialize()

    def initialize(self):
        self.initialize_grid()
        self.load_json_levels()
        self.initialize_sprite()
        self.picked_level = self.levels[1] #random.choice(self.levels)
        self.rooms_with_maps()
        self.setup_map()
    
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

    def get_sprite(self, x, y, sprite_sheet):
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((0,0,0))
        sprite.blit(sprite_sheet, (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
        return pygame.transform.scale(sprite, (SCALE_SIZE, SCALE_SIZE))

    def convert_pixelarray(self, pxarray):
        array = []
        for i in range(len(pxarray)):
            array.append([])
            for j in range(len(pxarray[i])):
                array[i].append(pxarray[i][j])
        
        return array

    def load_json_levels(self):
        folder = os.path.join(ROOT, LEVELS_FOLDER)
        for filename in os.listdir(folder):
            file = os.path.join(ROOT, LEVELS_FOLDER, filename)
            json_file = open('{}'.format(file))
            data = json.load(json_file)
            level = Level_CONFIG(data)
            self.levels.append(level)

    def rooms_with_maps(self):
        self.picked_rooms = [0, 1]

    def initialize_sprite(self):
        for y in range(0, self.sprite_sheet_rect.height, TILE_SIZE):
            for x in range(0, self.sprite_sheet_rect.width, TILE_SIZE):
                image = self.get_sprite(x, y, self.sprite_sheet)
                SPRITES.append(image)

    def initialize_grid(self):
        self.grid = []
        for i in range(DIM * DIM):
            self.grid.append(Room(i))
            
        
    def setup_map(self):
        self.level_sprites = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        self.items = []
        random_level = self.levels[1]
        self.grid[0].set_level(self.items, random_level, self.level_sprites, self.collision_group, SPRITES, self.levels.index(random_level), 0, 0, self.picked_rooms)
        for j in range(self.DIM):
            for i in range(self.DIM):
                index = i + j * self.DIM
                if not self.grid[index].collapsed:
                    last_index = (i - 1) + j * self.DIM
                    room_type = self.grid[last_index].room_type
                    if room_type == 1:
                        random_level = self.levels[0]
                        self.grid[index].set_level(self.items, random_level, self.level_sprites, self.collision_group, SPRITES, self.levels.index(random_level), i, j, self.picked_rooms)
            # to be fixed with a grid later on
            # currentX = (64 * 15) * (i + 1)
            # currentY = 0              
    
    def run(self, player):
        # print(len(self.level_sprites.sprites()), len(self.collision_group.sprites()))
        self.level_sprites.update(self.world_shift, 0)
        self.level_sprites.draw(self.display_surface)
        for item in self.items:
            item.update(self.world_shift, 0)
            item.draw()

        # outline for collition rect
        # for sprite in self.collision_group.sprites():
        #     pygame.draw.rect(self.display_surface, (0, 255, 0), sprite.rect, 1)
        self.scroll_X(player)
    