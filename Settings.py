from turtle import width
from pygame.math import Vector2

FPS = 60
PLAYER_SPEED = 5
FULL_SCREEN = False
SCREEN_WIDTH = 1600 if not FULL_SCREEN else 1600 #64 * 17
SCREEN_HEIGHT = 896 if not FULL_SCREEN else 900 #64 * 12
ROOM_WIDTH, ROOM_WIDTH_TILES = 64 * 23, 23
ROOM_HEIGHT, ROOM_HEIGHT_TILES = 64 * 12, 12
ROOM_OFFSET_X, ROOM_OFFSET_Y = 1, 1
TILE_SIZE = 32
DIM = 1
SCALE_SIZE = TILE_SIZE * 2
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)] # (x, y) UP, RIGHT, DOWN, LEFT
ENTROPY_DICT = { 0 : 2, 1 : 3, 2 : 0, 3 : 1}
GAME_LAYERS = ["LEVEL", "DECORATION"]
SPRITESHEET_LAYOUT = {
    "First_Layout": {
        "Constraints" : {
            "Width" : 544,
            "Height" : 352
        },
        "Collide" : {
            "From" : (0, 0),
            "To" : (512, 128),
            "Interact" : True
        },
        "Decoration" : {
            "From" : (0, 192),
            "To" : (512, 320),
            "Interact" : False
        }
    },
    "Second_Layout" : {
        "Constraints" : (),
        "Collide" : {
            "From" : (0, 0),
            "To" : ()
        },
        "Decoration" : {
            "From": (),
            "To" : ()
        }
    }
}

ITEMS_TRACK = {
    "Chest" : {
        "max" : 5,
        "current": 0,
        "per_room" : 2,
        "requirements" : [[0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 0], [1, 1, 1, 0]],
        "offset" : (0, 0)
    }   
}

DECORATIONS_TRACK = {
    "Door" : {
        "max" : 10,
        "current" : 0,
        "per_room" : 1,
        "requirements" : [[0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 0], [1, 1, 1, 0]],
        "offset" : (0, 1)
    }
}
