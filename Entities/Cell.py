from Entities.Decorations import *
from Entities.Tile import *
from Entities.Items import *
from Settings import *
import random


class Room:
    def __init__(self, index, infinite_list, single_list, SPRITES, all_tiles, collsion_tiles, level=None):
        self.index = index
        self.width, self.height = ROOM_WIDTH, ROOM_HEIGHT
        self.level = level
        self.sprites = SPRITES
        self.collapsed = False
        self.room_type = None
        self.currentX, self.currentY = 0, 0
        self.infinte_list, self.single_list = infinite_list, single_list
        self.all_tiles, self.tiles_collision = all_tiles, collsion_tiles
        self.room_tiles = [[None for j in range(ROOM_WIDTH)] for i in range(ROOM_HEIGHT)]
        self.items_in_room, self.decorations_in_room = [], []
        self.chest = Chest(64, 64, False, True, 1 * SCALE_SIZE, 4 * SCALE_SIZE)

    def get_position(self):
        conditions = [0, 0, 0, 0]
        current_position = pygame.math.Vector2(0, 0)
        for y in range(len(self.room_tiles)):
            for x in range(len(self.room_tiles[y])): 
                if y > 0:
                    lookup = self.room_tiles[y - 1][x]
                    return
                
                if x < (DIM - 1):
                    lookright = self.room_tiles[y][x + 1]
                    return
                
                if y < (DIM - 1):
                    lookdown = self.room_tiles[y + 1][x]
                    return
                
                if x > 0:
                    lookleft = self.room_tiles[y][x - 1]
                    return
                
        return 0, 0

    def generate_decorations(self):
        self.decorations_names = list(DECORATIONS_TRACK.keys())
        for name in DECORATIONS_TRACK:
            current_decoration = DECORATIONS_TRACK[name]
            spawn = random.randrange(0, 6)
            if spawn in [1, 3]:
                self.door = Door(41, 64, False, True, 2 * SCALE_SIZE, 6 * SCALE_SIZE)
                return
            
    
    def generate_items(self):
        self.items_names = list(ITEMS_TRACK.keys())
        for name in ITEMS_TRACK:
            current_item = ITEMS_TRACK[name]
            spawn = random.randrange(0, 6)
            if spawn in [1, 3]:
                return
        return

    def set_level(self, level, room_type, i, j):
        self.level = level
        self.collapsed = True
        self.room_type = room_type
        self.position = (i * self.width, j * self.height)
        self.trigger_draw()
        # self.single_list.append(self.door)
        # self.single_list.append(self.chest)

    def trigger_draw(self):
        for x in range(len(self.level.collide_layer)):
            tile_index = self.level.collide_layer[x] - 1
            tile = Tile(self.currentX, self.currentY, self.position, self.sprites[tile_index])
            if (tile_index <= 174 or tile_index in [420, 421, 422, 423, 455, 456, 457, 458]) and tile_index != 36:
                tile.set_colision(True)
                self.tiles_collision.add(tile)
            self.all_tiles.add(tile); 
            self.room_tiles[self.currentY][self.currentX] = tile
            self.currentX += 1
            if self.currentX >= self.level.room_width:
                self.currentY += 1
                self.currentX = 0
            