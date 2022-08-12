from itertools import count
from pygame.math import Vector2
import sys, os, pygame, numpy
from Settings import * 



ROOT = os.path.dirname(sys.modules['__main__'].__file__)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, image, x, y):
        super().__init__(group)
        self.x, self.y = x, y
        self.image = image
        self.rect = pygame.Rect((x, y), (TILE_SIZE, TILE_SIZE))
    


class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    def __init__(self):
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.level_sprites = pygame.sprite.Group()
        self.grid = []
        self.sprites = {}
        self.BLANK, self.UP, self.RIGHT, self.DOWN, self.LEFT = 0, 1, 2, 3, 4
        
    
    def setup_grid(self):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            self.grid.append([])
            self.grid[int(y/TILE_SIZE)].extend(-1 for i in range(int(SCREEN_WIDTH/TILE_SIZE)))                

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
    
    def setup_sprites(self):
        sprite_name, index = "Sprite_", 0
        for y in range(0, self.sprite_sheet.get_rect().h, TILE_SIZE):
            for x in range(0, self.sprite_sheet.get_rect().w, TILE_SIZE):
                image = self.get_sprite(x, y)
                pxarray = self.convert_pixelarray(pygame.PixelArray(image))
                if numpy.count_nonzero(pxarray) > 1:
                    self.sprites[sprite_name + str(index)] = {}
                    self.sprites[sprite_name + str(index)]["Position"] = None
                    self.sprites[sprite_name + str(index)]["sides"] = {}
                    self.sprites[sprite_name + str(index)]["Position"] = (x, y)
                    self.sprites[sprite_name + str(index)]["sides"][0] = pxarray[0]
                    self.sprites[sprite_name + str(index)]["sides"][1] = [array[0] for array in pxarray]
                    self.sprites[sprite_name + str(index)]["sides"][2] = pxarray[31]
                    self.sprites[sprite_name + str(index)]["sides"][3] = [array[31] for array in pxarray]
                    index += 1
                
    def generate_map(self):
        self.setup_grid()
        self.setup_sprites()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == -1:
                    return
        return
    
    def run(self, dt):
        self.generate_map()
        self.display_surface.fill("black")
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
        self.level_sprites.empty()
    