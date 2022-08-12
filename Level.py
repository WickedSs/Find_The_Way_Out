from itertools import count
from pygame.math import Vector2
import sys, os, pygame, numpy
from Settings import * 



ROOT = os.path.dirname(sys.modules['__main__'].__file__)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, image, x, y, pxarray):
        super().__init__(group)
        self.x, self.y = x, y
        self.image = image
        self.rect = pygame.Rect((x, y), (TILE_SIZE, TILE_SIZE))
        self.pxarray = pxarray
        # self.sides = { 0: [], 1: [], 2: [], 3: [] } # top right bottom left
    


class Level:
    spritesheet_filename = os.path.join(ROOT, "Assets/Spritesheet.png")
    def __init__(self):
        self.sprite_sheet = pygame.image.load(self.spritesheet_filename).convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.level_sprites = pygame.sprite.Group()
        self.sprites = {}
        
    
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
        
        print(self.sprites)           
        
        
    
    def run(self, dt):
        self.display_surface.fill("black")
        self.setup_sprites()
        print(self.level_sprites.sprites()[0].image)
        self.level_sprites.draw(self.display_surface)
        self.level_sprites.update(dt)
        self.level_sprites.empty()
    