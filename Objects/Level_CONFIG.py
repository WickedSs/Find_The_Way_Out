import os, sys


class Level_CONFIG:
    def __init__(self, data):
        self.data = data
        self.load_json()
    
    def load_json(self):
        self.collide_layer = self.data["layers"][0]["data"]
        self.background_layer = self.data["layers"][1]["data"]
        self.tile_width, self.tile_height = self.data["tilewidth"], self.data["tileheight"]
        self.room_width, self.room_height = self.data["width"], self.data["height"]
    