from Entities.Decorations import *
from Entities.Tile import *
from Entities.Items import *
from Settings import *
import random, operator


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
        self.room_tiles = [[None for j in range(ROOM_WIDTH_TILES)] for i in range(ROOM_HEIGHT_TILES)]
        self.items_in_room, self.decorations_in_room = [], []
        # self.chest = Chest(64, 64, False, True, 1 * SCALE_SIZE, 4 * SCALE_SIZE)

    def get_position(self, requirements):
        conditions, side = [0, 0, 0, 0], ""
        possible_position = []
        for y in range(ROOM_HEIGHT_TILES):
            for x in range(ROOM_WIDTH_TILES):
                if not self.room_tiles[y][x].collision and self.room_tiles[y][x].index != 36:
                    if y > 0:
                        lookup = self.room_tiles[y - 1][x]
                        if lookup.collision:
                            conditions[0] = 1
                    
                    if x < (ROOM_WIDTH_TILES - 1):
                        lookright = self.room_tiles[y][x + 1]
                        if lookright.collision:
                            conditions[1] = 1
                            side = "Right"
                    
                    if y < (ROOM_HEIGHT_TILES - 1):
                        lookdown = self.room_tiles[y + 1][x]
                        if lookdown.collision:
                            conditions[2] = 1
                    
                    if x > 0:
                        lookleft = self.room_tiles[y][x - 1]
                        if lookleft.collision:
                            conditions[3] = 1
                            side = "Left"
                    
                    if conditions in requirements:
                        possible_position.append((x, y, side))
                            
                    conditions = [0, 0, 0, 0]
                    side = ""
        
        return possible_position

    def generate_decorations(self):
        self.decorations_names = list(DECORATIONS_TRACK.keys())
        for name in DECORATIONS_TRACK:
            current_decoration = DECORATIONS_TRACK[name]
            requirements = current_decoration["requirements"]
            iterations = current_decoration["per_room"]
            positions = self.get_position(requirements)
            for iteration in range(iterations):
                spawn = random.randrange(0, 6)
                random_position = random.choice(positions)
                side = random_position[2]
                random_offset = tuple(map(operator.sub, random_position, current_decoration["offset"]))
                if spawn in [1, 3, 5]:
                    door_x, door_y = (random_offset[0] * SCALE_SIZE) + self.position[0], (random_offset[1] * SCALE_SIZE) + self.position[1]
                    print("Door: ", spawn, random_position, side, random_offset, self.position, door_x, door_y)
                    self.door = Door(41, 64, False, True, side, door_x, door_y)
                    self.single_list.add(self.door)
                    positions.remove(random_position)
            
    
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
        # for y in range(ROOM_HEIGHT_TILES):
            # print("Row: ", y, [tile.collision for tile in self.room_tiles[y]])
        # self.single_list.append(self.door)
        # self.single_list.append(self.chest)

    def trigger_draw(self):
        for x in range(len(self.level.collide_layer)):
            tile_index = self.level.collide_layer[x] - 1
            tile = Tile(self.currentX, self.currentY, self.position, self.sprites[tile_index], tile_index)
            if (tile_index <= 174 or tile_index in [420, 421, 422, 423, 455, 456, 457, 458]) and tile_index != 36:
                tile.set_colision(True)
                self.tiles_collision.add(tile)
            self.all_tiles.add(tile); 
            self.room_tiles[self.currentY][self.currentX] = tile
            self.currentX += 1
            if self.currentX >= self.level.room_width:
                self.currentY += 1
                self.currentX = 0
                
        self.generate_decorations()
            