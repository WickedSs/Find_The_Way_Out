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
    def __init__(self, x, y, image, edges):
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x * TILE_SIZE, self.y * TILE_SIZE
        self.edges = edges
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

        
        print(self.up, self.right, self.down, self.left)
    

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

# E4$yP4$$c0d3

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
    example_file_01 = os.path.join(ROOT, "Assets/Example-01.png")
    rules_file = os.path.join(ROOT, "Rules.xml")
    def __init__(self):
        global SPRITES
        self.display_surface = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.rules = ET.parse(self.rules_file)
        self.level_sprites = pygame.sprite.Group()
        self.layout_in_use = "First_Layout"
        self.index = 0
        SPRITES = [

            Tile(44, 0, self.get_sprite(1, 1), ["000, LLM", "000", "000", "000"]),
            # 0 0
            Tile(0, 0, self.get_sprite(0, 0), ["ABB, IHG", "JCD", "EFF", "FFA"]),
            Tile(1, 0, self.get_sprite(0, 0), ["ABB, IHG", "JCD", "EFF", "FFA"]).flip(True, False),
            Tile(0, 1, self.get_sprite(0, 0), ["ABB, IHG", "JCD", "EFF", "FFA"]).flip(False, True),
            Tile(1, 1, self.get_sprite(0, 0), ["ABB, IHG", "JCD", "EFF", "FFA"]).flip(True, True),
            
            # # 1 0
            Tile(3, 0, self.get_sprite(1, 0), ["BBB, IHG", "JCK, NCB, DCJ", "LLM, 000", "NCB, KCJ, JCD"]),
            Tile(3, 1, self.get_sprite(1, 2), ["NON, 000", "KCJ", "BBB", "JCK"]),
            
            # Tile(3, 0, self.get_sprite(1, 6), ["GHI", "IJJ", "JJJ", "JJK"]),
            # Tile(3, 1, self.get_sprite(1, 6), ["GHI", "IJJ", "JJJ", "JJK"]).flip(False, True),

            # # 0 1
            # Tile(5, 0, self.get_sprite(0, 1), ["CCC", "GGG", "CCC", "HHH"]),
            # Tile(5, 1, self.get_sprite(2, 1), ["CCC", "HHH", "CCC", "GGG"]),

            # # 4 0
            # Tile(7, 0, self.get_sprite(4, 0), ["III", "DDD", "JJJ", "DDD"]),
            # Tile(7, 1, self.get_sprite(4, 0), ["III", "DDD", "JJJ", "DDD"]).flip(False, True),
            
            # # 4 1
            # Tile(9, 0, self.get_sprite(4, 1), ["KKK", "KKK", "KKK", "KKK"]),

            # # 4 2
            # Tile(11, 0, self.get_sprite(4, 2), ["KKK", "EEE", "KKK", "KKK"]),
            # Tile(11, 1, self.get_sprite(4, 2), ["KKK", "EEE", "KKK", "KKK"]).flip(False, True),

            # # 6 0
            # Tile(13, 0, self.get_sprite(6, 0), ["LLL", "DDD", "DDD", "000"]),
            # Tile(13, 1, self.get_sprite(6, 0), ["LLL", "DDD", "DDD", "000"]).flip(True, False),

            # # 6 1
            # Tile(15, 0, self.get_sprite(6, 1), ["CCC", "DDD", "LLL", "000"]),
            # Tile(15, 1, self.get_sprite(6, 1), ["CCC", "DDD", "LLL", "000"]).flip(True, False),


            # Tile(17, 0, self.get_sprite(9, 0), ["MMM", "NNN", "CCC", "DDD"]),
            # Tile(17, 1, self.get_sprite(10, 1), ["EEE", "DDD", "KKK", "DDD"]),
            # Tile(18, 0, self.get_sprite(10, 0), ["CCC", "QQQ", "CCC", "000"]),
            # Tile(18, 1, self.get_sprite(9, 1), ["CCC", "000", "CCC", "RRR"]),
            
            # Tile(20, 0, self.get_sprite(12, 0), ["MMM", "VVV", "YYY", "RRR"]),
            # Tile(21, 0, self.get_sprite(13, 0), ["MMM", "QQQ", "YYY", "RRR"]),

            # Tile(20, 1, self.get_sprite(12, 1), ["WWW", "XXX", "KKK", "RRR"]),
            # Tile(21, 1, self.get_sprite(13, 1), ["WWW", "XXX", "KKK", "RRR"]),

            # Tile(22, 0, self.get_sprite(15, 0), ["MMM", "RRR", "WWW", ""]),
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
    
    def parse_rules(self):
        root = self.rules.getroot()
        for tile in root:
            print(tile.tag, tile.attrib)

    def checkValid(self, array, valid):
        for i in range(len(array)):
            try:
                element = array[i]
                if element not in valid:
                    array.remove(i) 
            except (IndexError, ValueError) as e:
                pass
        
        return array

    def setup_adjacency(self):
        for sprite in SPRITES:
            sprite.analyze()

    def initialize_grid(self):
        for i in range(DIM * DIM):
            cell = Cell(index=i)
            GRID.append(cell)

    def initialize_generation(self):

        # initialize grid and sprites into json array
        self.parse_rules()
        # self.initialize_grid()
        # self.setup_adjacency()
        sys.exit(1)

        GRID[0].collapsed = True
        GRID[0].options = [0]

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
                        print(len(working_cell.options))
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
                        options = [i for i in range(len(SPRITES))]
                        if y > 0:
                            validOptions = []
                            lookup = GRID[x + (y - 1) * DIM]
                            for option in lookup.options:
                                valid = SPRITES[option].down
                                validOptions.extend(valid)
                            options = self.checkValid(options, validOptions);
                        
                        if x < (DIM - 1):
                            validOptions = []
                            lookright = GRID[( x + 1 ) + y  * DIM]
                            for option in lookright.options:
                                valid = SPRITES[option].left
                                validOptions.extend(valid)
                            options = self.checkValid(options, validOptions);
                        
                        if y < (DIM - 1):
                            validOptions = []
                            lookdown = GRID[x + (y + 1) * DIM]
                            for option in lookdown.options:
                                valid = SPRITES[option].up
                                validOptions.extend(valid)
                            options = self.checkValid(options, validOptions);

                        if x > 0:
                            validOptions = []
                            lookleft = GRID[( x - 1 ) + y * DIM]
                            for option in lookleft.options:
                                valid = SPRITES[option].right
                                validOptions.extend(valid)
                            options = self.checkValid(options, validOptions);
                        
                        nextGrid[index] = Cell(index)
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
    