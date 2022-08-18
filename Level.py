from math import ceil
from multiprocessing.resource_sharer import stop
from pickle import TRUE
from textwrap import indent
from tkinter import Grid
from tkinter.tix import IMAGE
from turtle import onclick
from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string, operator
from Settings import *


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
SPRITES = []
GRID = []
VISITED = []
DIM = 15


class Tile:
    def __init__(self, x, y, image, edges):
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x * TILE_SIZE, self.y * TILE_SIZE
        self.edges = edges
        
    def rotate(self, angle):
        new_image = pygame.transform.rotate(self.image, 90 * angle)
        new_edges = []
        length = self.edges.length;
        for i in range(length):
            new_edges[i] = self.edges[(i - angle + length) % length];
        return Tile(self.x, self.y, new_image, new_edges)
    
    def flip(self, x_axis, y_axis):
        new_image = pygame.transform.flip(self.image, x_axis, y_axis)
        new_edges = self.edges
        if x_axis:
            new_edges[3], new_edges[1] = new_edges[1], new_edges[3]
        if y_axis:
            new_edges[0], new_edges[2] = new_edges[2], new_edges[0]
            
        return Tile(self.x, self.y, new_image, new_edges)


class Cell:
    def __init__(self, index):
        self.index = index
        self.collapsed = False
        self.options = [sprite for sprite in SPRITES]
    
    def rotate(self):
        return
    
    def set_options(self, options):
        self.options = options
    


class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    example_file_01 = os.path.join(ROOT, "Assets/Example-01.png")
    def __init__(self):
        global SPRITES
        self.display_surface = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.level_sprites = pygame.sprite.Group()
        self.layout_in_use = "First_Layout"
        SPRITES = [
            Tile(0, 0, self.get_sprite(0, 0), ["AAA", "BBB", "CCC", "DDD"]),
            Tile(1, 0, self.get_sprite(0, 0), ["AAA", "BBB", "CCC", "DDD"]).flip(True, False),
            Tile(0, 1, self.get_sprite(0, 0), ["AAA", "BBB", "CCC", "DDD"]).flip(False, True),
            Tile(1, 1, self.get_sprite(0, 0), ["AAA", "BBB", "CCC", "DDD"]).flip(True, True),
            
            # Tile(1, 0, self.get_sprite(1, 0), [], )
        ]
        self.initialize_generation()
    
    def get_sprite(self, x, y):
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return sprite

    def process_sides(self, pxarray):
        self.sides[0].extend(pxarray[0])
        self.sides[2].extend(pxarray[31])
        self.sides[1].extend(array[0] for array in pxarray)
        self.sides[3].extend(array[31] for array in pxarray)
    
    def convert_pixelarray(self, pxarray):
        array = []
        for i in range(len(pxarray)):
            array.append([])
            for j in range(len(pxarray[i])):
                array[i].append(pxarray[i][j])
        
        return array
    
    def common_sides(self, list1, list2):
        return [element for element in list1 if element in list2]
    
    def common_elements(self, list1, list2):
        max_identical = TILE_SIZE * TILE_SIZE
        identical = 0
        for y in range(len(list1)):
            for x in range(len(list1[y])):
                if list1[y][x] == list2[y][x]:
                    identical += 1

        return (identical * 100) / max_identical
    
    def initialize_grid(self):
        for i in range(DIM * DIM):
            cell = Cell(index=i)
            GRID.append(cell)

    def get_sprite_neighbours(self, x, y, array):
        x, y, neighbours = int(x / TILE_SIZE), int(y / TILE_SIZE), array
        if x > 0:
            working_x, working_y = x - 1, y
            neighbours[3].append((working_x, working_y))
        
        if x < (self.sprite_sheet_rect.width / TILE_SIZE) - 1:
            working_x, working_y = x + 1, y
            neighbours[1].append((working_x, working_y))
        
        if y > 0:
            working_x, working_y = x, (y - 1) 
            neighbours[0].append((working_x, working_y))

        if y < (self.sprite_sheet_rect.height  / TILE_SIZE) - 1:
            working_x, working_y = x, (y + 1)
            neighbours[2].append((working_x, working_y))
        
        return neighbours

    def initialize_generation(self):
        # initialize grid and sprites into json array
        self.initialize_grid()

        # Initial state
        # arr = numpy.arange(15*15).reshape(15, 15)
        # alist = [arr[0,:-1], arr[:-1,-1], arr[-1,::-1], arr[-2:0:-1,0]]
        # numpy.concatenate(alist)
        # for array in alist:
        #     for index in array:
        #         GRID[index].collapsed = True
        #         GRID[index].options = [SPRITES[12]]
        

    def run(self, dt):
        global SPRITES, GRID, VISITED, DIM
        self.display_surface.fill("black")

        for y in range(DIM):
            for x in range(DIM):
                working_cell = GRID[x + y * DIM]
                if working_cell.collapsed:
                    if working_cell.options:
                        sprite = working_cell.options[0]
                        self.display_surface.blit(sprite["Image"], (x * TILE_SIZE, y * TILE_SIZE))
        
        #  pick cell with the least entropy
        GRIDCOPY = GRID.copy();
        GRIDCOPY = list(filter(lambda x: x.collapsed == False, GRIDCOPY))
        GRIDCOPY.sort(key = lambda x : len(x.options))
        
        GRIDCOPY = []
        if len(GRIDCOPY) > 0:
            length, stopIndex = len(GRIDCOPY[0].options), 0
            for i in range(1, len(GRIDCOPY), 1):
                if len(GRIDCOPY[i].options) > length:
                    stopIndex = i;
                    break
            
            if stopIndex > 0: 
                GRIDCOPY = GRIDCOPY[0:stopIndex]
            picked_cell = random.choice(GRIDCOPY)
            picked_cell.collapsed = True
            pick = random.choice(picked_cell.options)
            picked_cell.options = [pick]

            nextGrid = [None for i in GRID]
            for y in range(DIM):
                for x in range(DIM):
                    index = x + y * DIM
                    if GRID[index].collapsed:
                        nextGrid[index] = GRID[index]
                    else:
                        if y > 0:
                            validSprites = []
                            lookup = GRID[x + (y - 1) * DIM]
                            for sprite in lookup.options:
                                validSprites.extend(sprite["Entropy"][2])
                        
                        if x < (DIM - 1):
                            validSprites = []
                            lookright = GRID[( x + 1 ) + y  * DIM]
                            for sprite in lookright.options:
                                validSprites.extend(sprite["Entropy"][3])
                        
                        if y < (DIM - 1):
                            validSprites = []
                            lookdown = GRID[x + (y + 1) * DIM]
                            for sprite in lookdown.options:
                                validSprites.extend(sprite["Entropy"][0])

                        if x > 0:
                            validSprites = []
                            lookleft = GRID[( x - 1 ) + y * DIM]
                            for sprite in lookleft.options:
                                validSprites.extend(sprite["Entropy"][1])
                        
                        nextGrid[index] = Cell(index)
                        nextGrid[index].collapsed = False
                        nextGrid[index].options = [SPRITES[valid] for valid in validSprites]
            
            GRID = nextGrid

        for sprite in SPRITES:
            print(sprite.edges)
            self.display_surface.blit(sprite.image, sprite.rect)
        sys.exit(1)
        # print(SPRITES[0]["Entropy"])
        # self.stupid_check(SPRITES[0])
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    