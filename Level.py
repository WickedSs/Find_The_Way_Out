from multiprocessing import current_process
from tkinter import Grid
from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string, operator
from Objects.Level_CONFIG import *
from Objects.Tile import *
from Settings import *
import xml.etree.ElementTree as ET
import json


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
LEVELS_FOLDER = "Assets/Levels"
SPRITES = []
GRID = []
VISITED = []
DIM = 8



    
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
        self.initialize()

    def initialize(self):
        # self.initialize_grid()
        self.load_json_levels()
        self.initialize_sprite()
        self.picked_level = self.levels[0] #random.choice(self.levels)
        self.setup_map()
    
    def scroll_X(self, player):
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < 200 and direction_x < 0:
            self.world_shift = PLAYER_SPEED
            player.speed = 0
        elif player_x > 1240 and direction_x > 0:
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
    
    def initialize_sprite(self):
        for y in range(0, self.sprite_sheet_rect.height, TILE_SIZE):
            for x in range(0, self.sprite_sheet_rect.width, TILE_SIZE):
                image = self.get_sprite(x, y, self.sprite_sheet)
                SPRITES.append(image)

    def initialize_grid(self):
        self.grid = []
        currentX, currentY = 0, 0
        for j in range(0, 768 * 2, 768):
            self.grid.append([])
            for i in range(0, 1440 * 2, 1440):
                self.grid[int(j / 768)].append([i, j])
        
    def setup_map(self):
        self.level_sprites = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        currentX, currentY = 0, 0 
        for x in range(len(self.picked_level.collide_layer)):
            tile_index = self.picked_level.collide_layer[x] - 1
            tile = Tile(currentX, currentY, SPRITES[tile_index])
            self.level_sprites.add(tile)
            if tile_index <= 174 and tile_index != 36:
                self.collision_group.add(tile)
            currentX += 1
            if currentX >= self.picked_level.room_width:
                currentY += 1
                currentX = 0

            # to be fixed with a grid later on
            # currentX = (64 * 15) * (i + 1)
            # currentY = 0              
    
    def run(self, player):
        self.level_sprites.update(self.world_shift, 0)
        self.level_sprites.draw(self.display_surface)
        self.scroll_X(player)
    