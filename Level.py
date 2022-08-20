from multiprocessing.resource_sharer import stop
from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string, operator
from Settings import *
import xml.etree.ElementTree as ET


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
LEVELS_FOLDER = "Assets/Levels"
SPRITES = []
GRID = []
VISITED = []
DIM = 8


class Tile:
    def __init__(self, x, y, image):
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x * TILE_SIZE, self.y * TILE_SIZE
        self.up, self.right, self.down, self.left = [], [], [], [] 

    def rotate(self, angle):
        new_image = pygame.transform.rotate(self.image, 90 * angle)
        new_edges = [None for i in self.edges]
        length = len(self.edges);
        for i in range(length):
            new_edges[i] = self.edges[(i - angle + length) % length];
        return Tile(self.x, self.y, new_image, new_edges)
    
    def flip(self, x_axis, y_axis):
        new_image = pygame.transform.flip(self.image, x_axis, y_axis)
        new_edges = self.edges

        # horizontal axis flipping
        if x_axis:
            # process left edges
            edges_left, edge_right = new_edges[3].split(","), new_edges[1].split(",")
            for cardinal in range(len(edges_left)):
                edges_left[cardinal] = edges_left[cardinal][::-1]            
            new_edges[3] = ",".join(input for input in edges_left)
            
            # process right edges
            for cardinal in range(len(edge_right)):
                edge_right[cardinal] = edge_right[cardinal][::-1]
            new_edges[1] = ",".join(input for input in edge_right)
            
            # set the new edges
            new_edges[3], new_edges[1] = new_edges[1], new_edges[3]
            new_edges[0], new_edges[2] = new_edges[0][::-1], new_edges[2][::-1]
        
        # vertical axis flipping
        if y_axis:
            # process up edges
            edges_up, edges_down = new_edges[0].split(","), new_edges[2].split(",")        
            for cardinal in range(len(edges_up)):
                edges_up[cardinal] = edges_up[cardinal].strip()[::-1]
     
            new_edges[0] = ",".join(input for input in edges_up)

            # process down edges
            for cardinal in range(len(edges_down)):
                edges_down[cardinal] = edges_down[cardinal].strip()[::-1]
            
            new_edges[2] = ",".join(input for input in edges_down)
            
            # set the new edges
            new_edges[0], new_edges[2] = new_edges[2], new_edges[0]
            new_edges[3], new_edges[1] = new_edges[3][::-1], new_edges[1][::-1]
            
        return Tile(self.x, self.y, new_image, new_edges)

class Cell:
    def __init__(self, index):
        self.index = index
        self.collapsed = False
        self.options = [i for i in range(len(SPRITES))]
            
    def rotate(self):
        return
    
    def set_options(self, options):
        self.options = options
    
class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    def __init__(self):
        global SPRITES
        self.display_surface = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.level_sprite_sheet = None
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.rules = ET.parse(self.rules_file)
        self.level_sprites = pygame.sprite.Group()
        self.layout_in_use = "First_Layout"
        self.index, self.levels, self.picked_level = 0, [], 0
        self.DEFAULT_OPTIONS = []
        self.load_levels()
        self.initialize_generation()
    
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

    def load_levels(self):
        folder = os.path.join(ROOT, LEVELS_FOLDER)
        for (dirpath, dirnames, filenames) in os.walk(folder):
            self.levels.extend(filenames)
    
    def initialize_sprite(self):
        constraints = SPRITESHEET_LAYOUT["First_Layout"]["Constraints"]
        for y in range(0, constraints["Height"], TILE_SIZE):
            for x in range(0, constraints["Width"], TILE_SIZE):
                image = self.get_sprite(x, y, self.sprite_sheet)
                pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                if numpy.count_nonzero(pxarray) > 1:
                    tile = Tile(x, y, image)
                    SPRITES.append(tile)

    def draw_level(self):
        for y in range(9):
            for x in range(15):
                currentX, currentY = x * TILE_SIZE, y * TILE_SIZE
                image = self.get_sprite(currentX, currentY, self.level_sprite_sheet)
                self.display_surface.blit(image, (currentX, currentY))
                
    
    def initialize_generation(self):
        self.initialize_sprite()
        self.picked_level = random.randrange(0, len(self.levels))
        level_path = os.path.join(ROOT, LEVELS_FOLDER, self.levels[self.picked_level])
        self.level_sprite_sheet = pygame.image.load(level_path).convert_alpha()
    
    def run(self, dt):
        global SPRITES, GRID, VISITED, DIM
        self.display_surface.fill("White")
        self.draw_level()
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    