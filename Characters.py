from fileinput import filename
from Settings import *
import os, sys

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
CHARACTERS_FOLDER = "Assets\Characters"


class CHARACATER:
    def __init__(self, name):
        self.character_name = name
        self.animations = {}
        self.load_animation()

    def load_animation(self):
        path = os.path.join(ROOT, CHARACTERS_FOLDER, self.character_name)
        for anim_folder in os.listdir(path):
            anim_name = anim_folder.split("-")[1]
            self.animations[anim_name] = {}
            self.animations[anim_name]["frames"] = []
            frames = os.path.join(ROOT, CHARACTERS_FOLDER, self.character_name, anim_folder)
            for frame in os.listdir(frames):
                self.animations[anim_name]["frames"].append(frame)
            


class Characters:
    def __init__(self):
        self.characters = []
        self.load_characters()
        print(self.characters)

    def load_characters(self):
        chars = os.path.join(ROOT, CHARACTERS_FOLDER)
        print(chars)
        for character_name in os.listdir(chars):
            Character = CHARACATER(character_name)
            self.characters.append(Character)
