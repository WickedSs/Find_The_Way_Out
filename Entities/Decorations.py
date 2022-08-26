import os, sys, pygame
from Entities.Item import Item


class Cannon:
    def __init__(self):
        pass


class Candle:
    def __init__(self):
        pass
    

class Chains:
    def __init__(self, x, y):
        pass

class Door(Item):
    def __init__(self, x, y, width, height):
        super().__init__(self, x, y, width, height)
        self.asset_name = "Big_Map"
        self.animation_type = "Multiple"
        self.x, self.y = x, y
        print(self.display_surface)

class Window:
    def __init__(self):
        pass

    
class Barrel_UP:
    def __init__(self):
        pass


class Barrel_Down:
    def __init__(self):
        pass
    

class Bottle_UP_1:
    def __init__(self):
        pass
    

class Bottle_UP_2:
    def __init__(self):
        pass
    

class Bottle_Down_1:
    def __init__(self):
        pass
    

class Bottle_Down_2:
    def __init__(self):
        pass