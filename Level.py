from pygame.math import Vector2
import sys, os, pygame, numpy, random, time, string, operator
from Settings import *
import elementpath
import xml.etree.ElementTree as ET


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
SPRITES = []
GRID = []
VISITED = []
DIM = 2


class Tile:
    def __init__(self, x, y, image):
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x * TILE_SIZE, self.y * TILE_SIZE
        self.up, self.right, self.down, self.left = [], [], [], []
    
    def reverseString(self, s):
        arr = s.split('');
        arr = arr.reverse();
        return arr.join('');

    def compareEdge(self, a, b):
        return len(list(set(a).intersection(b)));

    def analyze(self):
        for i in range(len(SPRITES)):
            tile = SPRITES[i];

            # UP
            vertical_tile, vertical_local = tile.edges[2].split(","), self.edges[0].split(",")
            if (self.compareEdge(vertical_tile, vertical_local) > 0):
                self.up.append(i);
            
            # RIGHT
            horizontal_tile, horizontal_local = tile.edges[3].split(","), self.edges[1].split(",")
            if (self.compareEdge(horizontal_tile, horizontal_local) > 0):
                self.right.append(i);
            
            # DOWN
            vertical_tile, vertical_local = tile.edges[0].split(","), self.edges[2].split(",") 
            if (self.compareEdge(vertical_tile, vertical_local) > 0):
                self.down.append(i);
            
            # LEFT
            horizontal_tile, horizontal_local = tile.edges[1].split(","), self.edges[3].split(",")
            if (self.compareEdge(horizontal_tile, horizontal_local) > 0):
                self.left.append(i);    

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
    def __init__(self, index, not_included):
        self.index = index
        self.collapsed = False
        self.not_included = not_included
        if self.not_included:
            self.options = [i for i in range(len(SPRITES)) if i not in self.not_included]
        else:
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
    
    def parse_rules(self):
        index = 0
        root = self.rules.getroot()
        for Rules in root:
            for rule in Rules.findall("Rule"):
                indexAttrib = list(rule.attrib.keys())[0]
                agencencyAttribs = list(rule.attrib.keys())[1:5]
                tileIndex = int(rule.get(indexAttrib))
                for agencency in agencencyAttribs:
                    agenciesList = rule.get(agencency).split(",")
                    if len(agenciesList[0]) > 0:
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
        
    def checkValid(self, array, valid):
        print(array, valid)
        if (valid):
            for i in range(len(array)):
                try:
                    element = array[i]
                    if element not in valid:
                        array.remove(i) 
                except (IndexError, ValueError) as e:
                    pass
        
        return array

    def initialize_grid(self):
        for i in range(DIM * DIM):
            cell = Cell(index=i, not_included=self.not_included)
            GRID.append(cell)

    def initialize_sprite(self):
        constraints = SPRITESHEET_LAYOUT["First_Layout"]["Constraints"]
        for y in range(0, constraints["Height"], TILE_SIZE):
            for x in range(0, constraints["Width"], TILE_SIZE):
                image = self.get_sprite(x, y)
                pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                if numpy.count_nonzero(pxarray) > 1:
                    tile = Tile(x, y, image)
                    SPRITES.append(tile)
                

    def initialize_generation(self):

        # initialize grid and sprites into json array
        self.initialize_sprite()
        self.initialize_grid()
        self.parse_rules()
        # print(len(SPRITES), len(GRID))

        GRID[0].collapsed = True
        GRID[0].options = [12]

        # Initial state
        # arr = numpy.arange(15*15).reshape(15, 15)
        # alist = [arr[0,:-1], arr[:-1,-1], arr[-1,::-1], arr[-2:0:-1,0]]
        # numpy.concatenate(alist)
        # for array in alist:
        #     for index in array:
        #         GRID[index].collapsed = True
        #         GRID[index].options = [SPRITES[0]]
        

    def run(self, dt):
        global SPRITES, GRID, VISITED, DIM
        self.display_surface.fill("White")

        for y in range(DIM):
            for x in range(DIM):
                working_cell = GRID[x + y * DIM]
                if working_cell.collapsed:
                    if working_cell.options:
                        sprite = working_cell.options[0]
                        self.display_surface.blit(SPRITES[sprite].image, (x * TILE_SIZE, y * TILE_SIZE))
        

        #  pick cell with the least entropy
        GRIDCOPY = GRID.copy();
        GRIDCOPY = list(filter(lambda x: x.collapsed == False, GRIDCOPY))
        GRIDCOPY.sort(key = lambda x : len(x.options))
        
        # GRIDCOPY = []
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
                        options = [i for i in range(len(SPRITES)) if i not in self.not_included]
                        if y > 0:
                            validOptions = []
                            lookup = GRID[x + (y - 1) * DIM]
                            for option in lookup.options:
                                valid = SPRITES[option].up
                                print("UP: ", valid)
                                validOptions.extend(valid)
                            options = self.checkValid(options, validOptions);
                        
                        if x < (DIM - 1):
                            validOptions = []
                            lookright = GRID[( x + 1 ) + y  * DIM]
                            for option in lookright.options:
                                valid = SPRITES[option].right
                                print("RIGHT: ", valid)
                                validOptions.extend(valid)
                            options = self.checkValid(options, validOptions);
                        
                        if y < (DIM - 1):
                            validOptions = []
                            lookdown = GRID[x + (y + 1) * DIM]
                            for option in lookdown.options:
                                valid = SPRITES[option].down
                                print("DOWN: ", valid)
                                validOptions.extend(valid)
                            options = self.checkValid(options, validOptions);

                        if x > 0:
                            validOptions = []
                            lookleft = GRID[( x - 1 ) + y * DIM]
                            for option in lookleft.options:
                                valid = SPRITES[option].left
                                print("LEFT: ", valid)
                                validOptions.extend(valid)
                            options = self.checkValid(options, validOptions);
                        
                        nextGrid[index] = Cell(index, self.not_included)
                        nextGrid[index].set_options(options)
                        
            
            GRID = nextGrid

        # for sprite in SPRITES:
        #     if self.index == 0:
        #         print(sprite.edges)
        #     self.display_surface.blit(sprite.image, sprite.rect)
        
        # self.index += 1
        # print(SPRITES[0]["Entropy"])
        # self.stupid_check(SPRITES[0])
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
    