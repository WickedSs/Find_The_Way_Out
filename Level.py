from multiprocessing.resource_sharer import stop
from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string, operator
from Settings import *
import elementpath
import xml.etree.ElementTree as ET


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
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
    rules_file = os.path.join(ROOT, "Rules.xml")
    def __init__(self):
        global SPRITES
        self.display_surface = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.rules = ET.parse(self.rules_file)
        self.level_sprites = pygame.sprite.Group()
        self.layout_in_use = "First_Layout"
        self.index, self.not_included = 0, []
        self.DEFAULT_OPTIONS = []
        self.initialize_generation()
    
    def get_sprite(self, x, y):
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
        
    def checkValid(self, array, valid):
        valid = list(set(valid))
        for i in range(len(array) - 1, -1, -1):
            element = array[i]
            if element not in valid:
                array.remove(element)
        
        return array

    def most_frequent(self, array):
        return max(set(array), key = array.count)

    def initialize_grid(self):
        for i in range(DIM * DIM):
            cell = Cell(index=i)
            GRID.append(cell)
        
        # Initial state of GRID
        alist, value, valueIdx = [0, 7, 56, 63], [4, 5, 15, 16], 0
        for index in alist:
            GRID[index].collapsed = True
            GRID[index].options = [value[valueIdx]]
            valueIdx += 1

    def initialize_sprite(self):
        constraints = SPRITESHEET_LAYOUT["First_Layout"]["Constraints"]
        for y in range(0, constraints["Height"], TILE_SIZE):
            for x in range(0, constraints["Width"], TILE_SIZE):
                image = self.get_sprite(x, y)
                pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                if numpy.count_nonzero(pxarray) > 1:
                    tile = Tile(x, y, image)
                    SPRITES.append(tile)
        
        self.DEFAULT_OPTIONS = [i for i in range(len(SPRITES))]
        index = 0
        root = self.rules.getroot()
        for Rules in root:
            for rule in Rules.findall("Rule"):
                indexAttrib = list(rule.attrib.keys())[0]
                agencencyAttribs = list(rule.attrib.keys())[1:5]
                tileIndex = int(rule.get(indexAttrib))
                for agencency in agencencyAttribs:
                    agenciesList = rule.get(agencency).split(",")
                    if len(agenciesList) > 0:
                        if agencency == "top":
                            SPRITES[tileIndex].up.extend([int(agency) for agency in agenciesList])
                        if agencency == "left":
                            SPRITES[tileIndex].left.extend([int(agency) for agency in agenciesList])
                        if agencency == "down":
                            SPRITES[tileIndex].down.extend([int(agency) for agency in agenciesList])
                        if agencency == "right":
                            SPRITES[tileIndex].left.extend([int(agency) for agency in agenciesList])
                    else:
                        self.not_included.append(index)
                
                index += 1

    def initialize_generation(self):
        self.initialize_sprite()
        self.initialize_grid()
    
    def run(self, dt):
        global SPRITES, GRID, VISITED, DIM
        self.display_surface.fill("White")

        for y in range(DIM):
            for x in range(DIM):
                cell = GRID[x + y * DIM]
                if cell.collapsed:
                    sprite = random.choice(cell.options)
                    self.display_surface.blit(SPRITES[sprite].image, (x * TILE_SIZE, y * TILE_SIZE))
                # else:
                #     self.display_surface.blit(SPRITES[12].image, (x * TILE_SIZE, y * TILE_SIZE))

        #  pick cell with the least entropy
        GRIDCOPY = GRID
        GRIDCOPY = list(filter(lambda x: x.collapsed == False, GRIDCOPY))
        GRIDCOPY.sort(key = lambda x : len(x.options))

        # GRIDCOPY = []
        if len(GRIDCOPY) > 0:
            length, stopIndex = len(GRIDCOPY[0].options), 0
            for i in range(1, len(GRIDCOPY), 1):
                if len(GRIDCOPY[i].options) > length:
                    stopIndex = i;
                    break
            
            if stopIndex > 0: GRIDCOPY = [GRIDCOPY[stopIndex]]
            cell = random.choice(GRIDCOPY)
            cell.collapsed = True
            pick = random.choice(cell.options)
            cell.options = [pick]
        
            nextGrid = [None for i in GRID]
            for y in range(DIM):
                for x in range(DIM):
                    index = x + y * DIM
                    if GRID[index].collapsed:
                        nextGrid[index] = GRID[index]
                    else:
                        validOptions = []
                        if y > 0:
                            lookup = GRID[x + (y - 1) * DIM]
                            if lookup.collapsed:
                                for option in lookup.options:
                                    valid = SPRITES[option].down
                                    validOptions.extend(valid)
                        
                        if x < (DIM - 1):
                            lookright = GRID[( x + 1 ) + y  * DIM]
                            if lookright.collapsed:
                                for option in lookright.options:
                                    valid = SPRITES[option].left
                                    validOptions.extend(valid)
                        
                        if y < (DIM - 1):
                            lookdown = GRID[x + (y + 1) * DIM]
                            if lookdown.collapsed:
                                for option in lookdown.options:
                                    valid = SPRITES[option].up
                                    validOptions.extend(valid)

                        if x > 0:
                            lookleft = GRID[( x - 1 ) + y * DIM]
                            if lookleft.collapsed:
                                for option in lookleft.options:   
                                    valid = SPRITES[option].right
                                    validOptions.extend(valid)
                        
                        validOptions = list(set(validOptions))
                        # validOptions = [self.most_frequent(validOptions)]
                        # print(x, y, "FINAL: ", validOptions)
                        nextGrid[index] = Cell(index)
                        nextGrid[index].set_options(validOptions)

            for grid in nextGrid:
                if len(grid.options) <= 0:
                    grid.set_options(self.DEFAULT_OPTIONS)
            GRID = nextGrid
            time.sleep(0.5)
            for i in range(DIM):
                for j in range(DIM):
                    index = i + j * DIM
                    print("GRID[", index, "]", nextGrid[index].options)
            # sys.exit(1)
            # print("NEXTGRID: ", [len(grid.options) for grid in nextGrid if not grid.collapsed], self.index)
        # for sprite in SPRITES:
        #     if self.index == 0:
        #         print(sprite.edges)
        #     self.display_surface.blit(sprite.image, sprite.rect)
        
        # self.index += 1
        # print(SPRITES[0]["Entropy"])
        # self.stupid_check(SPRITES[0])
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    