from math import ceil
from pickle import TRUE
from textwrap import indent
from tkinter import Grid
from tkinter.tix import IMAGE
from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string
from Settings import *
import operator
from itertools import chain


alphabet = string.ascii_letters
ROOT = os.path.dirname(sys.modules['__main__'].__file__)
SPRITES = []
GRID = []
VISITED = []
DIM = 10


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
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.display_surface = pygame.display.get_surface()
        self.level_sprites = pygame.sprite.Group()
        self.queue, self.sprites = [], [[None for j in range(15)] for i in range(9)]
        self.layout_in_use = "First_Layout"
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
    
    def stupid_check(self, sprite):
        Entropy = sprite["Entropy"]
        Image = sprite["Image"]
        self.display_surface.blit(Image, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        x, y = 32, SCREEN_HEIGHT / 2
        for i in range(4):
            for spr in Entropy[i]:
                self.display_surface.blit(SPRITES[spr]["Image"], (x, y))
                x += 32
                if x >= SCREEN_HEIGHT:
                    x = 32
                    y += 32


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
            index = 0
            for y in range(0, constraints["Height"], TILE_SIZE):
                for x in range(0, constraints["Width"], TILE_SIZE):
                    image = self.get_sprite((x, y))
                    pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                    if numpy.count_nonzero(pxarray) > 1:
                        top, right, down, left = pxarray[0], [array[31] for array in pxarray], pxarray[31], [array[0] for array in pxarray]
                        if top == down_sprite:
                            entropy_sprite[ENTROPY_DICT[0]].append(index)
                        if right == left_sprite:
                            entropy_sprite[ENTROPY_DICT[1]].append(index)
                        if down == top_sprite:
                            entropy_sprite[ENTROPY_DICT[2]].append(index)
                        if left == right_sprite:
                            entropy_sprite[ENTROPY_DICT[3]].append(index)
                        
                        index += 1
            
        
        
        for sprite in SPRITES:
            del sprite["Pixels"]
            # print(SPRITES.index(sprite), sprite)


        
    def initialize_generation(self):
        # initialize grid and sprites into json array
        self.initialize_sprites()
        self.initialize_grid()
        

    def run(self, dt):
        global SPRITES, GRID, VISITED, DIM
        self.display_surface.fill("black")
        
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
                        validSprites = []
                        if y > 0:
                            lookup = GRID[x + (y - 1) * DIM]
                            for sprite in lookup.options:
                                validSprites.extend(sprite["Entropy"][2])
                        
                        if x < (DIM - 1):
                            lookright = GRID[( x + 1 ) + y  * DIM]
                            for sprite in lookright.options:
                                validSprites.extend(sprite["Entropy"][3])
                        
                        if y < (DIM - 1):
                            lookdown = GRID[x + (y + 1) * DIM]
                            for sprite in lookdown.options:
                                validSprites.extend(sprite["Entropy"][0])

                        if x > 0:
                            lookleft = GRID[( x - 1 ) + y * DIM]
                            for sprite in lookleft.options:
                                validSprites.extend(sprite["Entropy"][1])
                        
                        validSprites = list(set([i for i in validSprites]))
                        nextGrid[index] = Cell(index)
                        nextGrid[index].collapsed = False
                        nextGrid[index].options = [SPRITES[valid] for valid in validSprites]
            
            GRID = nextGrid

        for y in range(DIM):
            for x in range(DIM):
                working_cell = GRID[x + y * DIM]
                if working_cell.collapsed:
                    sprite = working_cell.options[0]
                    self.display_surface.blit(sprite["Image"], (x * TILE_SIZE, y * TILE_SIZE))

        print(SPRITES[0]["Entropy"])
        self.stupid_check(SPRITES[0])
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    