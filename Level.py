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
        # self.rules = ET.parse(self.rules_file)
        self.level_sprites = pygame.sprite.Group()
        self.layout_in_use = "First_Layout"
        self.index, self.levels, self.picked_level = 0, [], 0
        self.initialize()

    def initialize(self):
        self.load_json_levels()
        self.initialize_sprite()
        self.picked_level = random.choice(self.levels)
    
    def get_sprite(self, x, y, sprite_sheet):
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((0,0,0))
        sprite.blit(sprite_sheet, (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
        return sprite

    def convert_pixelarray(self, pxarray):
        array = []
        for i in range(len(pxarray)):
            array.append([])
            for j in range(len(pxarray[i])):
                array[i].append(pxarray[i][j])
        
        return array

    def load_json_levels(self):
        folder = os.path.join(ROOT, LEVELS_FOLDER)
        for (dirpath, dirnames, filenames) in os.walk(folder):
            for filename in filenames:
                file = os.path.join(ROOT, LEVELS_FOLDER, filename)
                json_file = open('{}'.format(file))
                data = json.load(json_file)
                level = Level_CONFIG(data)
                self.levels.append(level)
    
    def initialize_sprite(self):
        constraints = SPRITESHEET_LAYOUT["First_Layout"]["Constraints"]
        for y in range(0, self.sprite_sheet_rect.height, TILE_SIZE):
            for x in range(0, self.sprite_sheet_rect.width, TILE_SIZE):
                image = self.get_sprite(x, y, self.sprite_sheet)
                tile = Tile(x, y, image)
                self.level_sprites.add(tile)
                SPRITES.append(tile)
        
    def draw_level(self):
        for y in range(self.picked_level.room_height):
            for x in range(self.picked_level.room_width):
                index = x + y * self.picked_level.room_width
                tile = self.picked_level.collide_layer[index] - 1
                currentX, currentY = x * self.picked_level.tile_width, y * self.picked_level.tile_height
                image = SPRITES[tile].image
                self.display_surface.blit(image, (currentX, currentY))
                
    
    def run(self, dt):
        global SPRITES, GRID, VISITED, DIM
        self.display_surface.fill("White")
        self.draw_level()
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    