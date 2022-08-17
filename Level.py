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


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.x, self.y = x, y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y


class Cell:
    def __init__(self, index):
        self.index = index
        self.collapsed = False
        self.options = [sprite for sprite in SPRITES]
    
    def set_options(self, options):
        self.options = options
    


class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    example_file_01 = os.path.join(ROOT, "Assets\Example-01.png")
    def __init__(self):
        global SPRITES
        self.display_surface = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.level_sprites = pygame.sprite.Group()
        self.layout_in_use = "First_Layout"
        SPRITES = [                                                                         #TOP     RIGHT       DOWN      LEFT 
            { "Index" : 0, "Image" : self.get_sprite((0 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [1, 2], 2 : [11], 3 : [] } },
            { "Index" : 1, "Image" : self.get_sprite((1 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [1, 2, 6], 2 : [0, 1, 6], 3 : [12] } },
            { "Index" : 2, "Image" : self.get_sprite((2 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [13], 3 : [0, 1] } },
            { "Index" : 3, "Image" : self.get_sprite((4 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [14], 3 : [] } },
            { "Index" : 4, "Image" : self.get_sprite((6 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [12], 1 : [24], 2 : [13, 46], 3 : [12] } },
            { "Index" : 5, "Image" : self.get_sprite((7 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [12], 1 : [12], 2 : [11, 45], 3 : [24] } },
            { "Index" : 6, "Image" : self.get_sprite((9 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [3], 1 : [1], 2 : [12], 3 : [1] } },
            { "Index" : 7, "Image" : self.get_sprite((10 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [13], 1 : [36, 32], 2 : [13], 3 : [12] } },
            { "Index" : 8, "Image" : self.get_sprite((12 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [3], 1 : [29], 2 : [27], 3 : [36] } },
            { "Index" : 9, "Image" : self.get_sprite((13 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [11], 3 : [] } },
            { "Index" : 10, "Image" : self.get_sprite((15 * TILE_SIZE, 0 * TILE_SIZE)), "Entropy" : { 0 : [3], 1 : [36], 2 : [14], 3 : [36] } },
            { "Index" : 11, "Image" : self.get_sprite((0 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [11], 3 : [] } },
            { "Index" : 12, "Image" : self.get_sprite((1 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [11], 3 : [] } },
            { "Index" : 13, "Image" : self.get_sprite((2 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [11], 3 : [] } },
            { "Index" : 14, "Image" : self.get_sprite((4 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [26], 3 : [] } },
            { "Index" : 15, "Image" : self.get_sprite((6 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [11], 3 : [] } },
            { "Index" : 16, "Image" : self.get_sprite((7 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [11], 3 : [] } },
            { "Index" : 17, "Image" : self.get_sprite((9 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [11], 1 : [12], 2 : [11], 3 : [36] } },
            { "Index" : 18, "Image" : self.get_sprite((10 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [12], 1 : [24], 2 : [26], 3 : [24] } },
            { "Index" : 19, "Image" : self.get_sprite((12 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 20, "Image" : self.get_sprite((13 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 21, "Image" : self.get_sprite((15 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 22, "Image" : self.get_sprite((16 * TILE_SIZE, 1 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 23, "Image" : self.get_sprite((0 * TILE_SIZE, 2 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 24, "Image" : self.get_sprite((1 * TILE_SIZE, 2 * TILE_SIZE)), "Entropy" : { 0 : [12], 1 : [25, 18], 2 : [], 3 : [23, 18] } },
            { "Index" : 25, "Image" : self.get_sprite((2 * TILE_SIZE, 2 * TILE_SIZE)), "Entropy" : { 0 : [13, 29], 1 : [], 2 : [], 3 : [24, 42] } },
            { "Index" : 26, "Image" : self.get_sprite((4 * TILE_SIZE, 2 * TILE_SIZE)), "Entropy" : { 0 : [14], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 27, "Image" : self.get_sprite((6 * TILE_SIZE, 3 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 28, "Image" : self.get_sprite((7 * TILE_SIZE, 3 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 29, "Image" : self.get_sprite((9 * TILE_SIZE, 3 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [37, 32], 2 : [], 3 : [30, 39] } },
            { "Index" : 30, "Image" : self.get_sprite((10 * TILE_SIZE, 3 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 31, "Image" : self.get_sprite((11 * TILE_SIZE, 3 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 32, "Image" : self.get_sprite((13 * TILE_SIZE, 3 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [36, 17], 2 : [26], 3 : [36, 7, 15] } },
            { "Index" : 33, "Image" : self.get_sprite((15 * TILE_SIZE, 2 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [36, 43, 37, 10], 2 : [26], 3 : [] } },
            { "Index" : 34, "Image" : self.get_sprite((16 * TILE_SIZE, 2 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [26], 3 : [36, 32, 35, 10] } },
            { "Index" : 35, "Image" : self.get_sprite((0 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [36, 45, 43, 32], 2 : [], 3 : [] } },
            { "Index" : 36, "Image" : self.get_sprite((1 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [37, 43, 46, 34], 2 : [], 3 : [35, 32, 45, 33] } },
            { "Index" : 37, "Image" : self.get_sprite((2 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [36, 32, 43, 45] } },
            { "Index" : 38, "Image" : self.get_sprite((4 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 39, "Image" : self.get_sprite((6 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 40, "Image" : self.get_sprite((7 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 41, "Image" : self.get_sprite((9 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 42, "Image" : self.get_sprite((10 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 43, "Image" : self.get_sprite((12 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [3], 1 : [36, 37], 2 : [], 3 : [36, 32] } },
            { "Index" : 44, "Image" : self.get_sprite((13 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [], 1 : [], 2 : [], 3 : [] } },
            { "Index" : 45, "Image" : self.get_sprite((15 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [3, 33], 1 : [43, 36, 32], 2 : [], 3 : [] } },
            { "Index" : 46, "Image" : self.get_sprite((16 * TILE_SIZE, 4 * TILE_SIZE)), "Entropy" : { 0 : [3, 34], 1 : [], 2 : [], 3 : [45, 36, 32] } },
        ]
        self.initialize_generation()
    
    def get_sprite(self, position):
        x, y = position
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
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


    def initialize_sprites(self):
        constraints= SPRITESHEET_LAYOUT["First_Layout"]["Constraints"]
        for y in range(0, constraints["Height"], TILE_SIZE):
            for x in range(0, constraints["Width"], TILE_SIZE):
                image = self.get_sprite((x, y))
                pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                if numpy.count_nonzero(pxarray) > 1:
                    SPRITES.append({
                        "Image" : image,
                        "Pixels" : pxarray,
                        "Entropy" : {
                            0 : [], # top
                            1 : [], # right
                            2 : [], # down
                            3 : []  # left
                        }
                    })


        for sprite in SPRITES:
            pxarray_sprite = sprite["Pixels"]
            entropy_sprite = sprite["Entropy"]
            top_sprite, right_sprite, down_sprite, left_sprite = pxarray_sprite[0], [pxsprite[31] for pxsprite in pxarray_sprite], pxarray_sprite[31], [pxsprite[0] for pxsprite in pxarray_sprite]
            index, least_identical = 0, 24
            for y in range(0, constraints["Height"], TILE_SIZE):
                for x in range(0, constraints["Width"], TILE_SIZE):
                    image = self.get_sprite((x, y))
                    pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                    if numpy.count_nonzero(pxarray) > 1:
                        top, right, down, left = pxarray[0], [array[31] for array in pxarray], pxarray[31], [array[0] for array in pxarray]
                        # print(self.common_elements(pxarray_sprite, pxarray))
                        print(len(self.common_sides(right_sprite, left)))
                        if len(self.common_sides(top, down_sprite)) >= least_identical:
                            entropy_sprite[ENTROPY_DICT[0]].append(index)
                        if len(self.common_sides(right, left_sprite)) >= least_identical:
                            entropy_sprite[ENTROPY_DICT[1]].append(index)
                        if len(self.common_sides(down, top_sprite)) >= least_identical:
                            entropy_sprite[ENTROPY_DICT[2]].append(index)
                        if len(self.common_sides(left, right_sprite)) >= least_identical:
                            entropy_sprite[ENTROPY_DICT[3]].append(index)
                        
                        if x == 32 * 6:
                            sys.exit(1)
                        index += 1
            

        
        for sprite in SPRITES:
            del sprite["Pixels"]
            # print(SPRITES.index(sprite), sprite)

    def initialize_generation(self):
        # initialize grid and sprites into json array
        # self.initialize_sprites()
        self.initialize_grid()

        # GRID[0].collapsed = True
        # GRID[0].options = [SPRITES[4]]
        

    def run(self, dt):
        global SPRITES, GRID, VISITED, DIM
        self.display_surface.fill("black")

        for y in range(DIM):
            for x in range(DIM):
                working_cell = GRID[x + y * DIM]
                if working_cell.collapsed:
                    sprite = SPRITES[12]
                    if working_cell.options:
                        sprite = working_cell.options[0]
                    self.display_surface.blit(sprite["Image"], (x * TILE_SIZE, y * TILE_SIZE))
        
        #  pick cell with the least entropy
        GRIDCOPY = GRID.copy();
        GRIDCOPY = list(filter(lambda x: x.collapsed == False, GRIDCOPY))
        GRIDCOPY.sort(key = lambda x : len(x.options))
        
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
            pick = None
            if picked_cell.options:
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

        # print(SPRITES[0]["Entropy"])
        # self.stupid_check(SPRITES[0])
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    