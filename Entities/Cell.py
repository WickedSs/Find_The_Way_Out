

from Entities.Tile import Tile
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Cell:
    def __init__(self, index, level=None):
        self.index = index
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.level = level
        self.collapsed = False
        self.room_type = None
        self.currentX, self.currentY = 0, 0
        self.room_tiles = []
        
            
    def set_level(self, level, tiles, tiles_collision, SPRITES, room_type, i, j):
        self.level = level
        self.collapsed = True
        self.room_type = room_type
        self.position = (i * self.width, j * self.height)
        self.trigger_draw(tiles, tiles_collision, SPRITES)
    
    def trigger_items(self):
        for i in range(2):
            return

    def trigger_draw(self, tiles, tiles_collision, SPRITES):
        for x in range(len(self.level.collide_layer)):
            tile_index = self.level.collide_layer[x] - 1
            tile = Tile(self.currentX, self.currentY, self.position, SPRITES[tile_index])
            tiles.add(tile); self.room_tiles.append(tile)
            if (tile_index <= 174 or tile_index in [420, 421, 422, 423, 455, 456, 457, 458]) and tile_index != 36 :
                tiles_collision.add(tile)
            self.currentX += 1
            if self.currentX >= self.level.room_width:
                self.currentY += 1
                self.currentX = 0