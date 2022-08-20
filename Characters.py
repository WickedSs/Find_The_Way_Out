from fileinput import filename
from Settings import *
import os, sys

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
CHARACTERS_FOLDER = "Assets\Characters"


class CHARACATER:
    def __init__(self, name):
        self.character_name = name
        self.animations = {}
        self.animations_folders = []
        self.load_animation()

    def load_animation(self):
        path = os.path.join(ROOT, CHARACTERS_FOLDER, self.character_name)
        for anim_folder in os.listdir(path):
            self.animations_folders.append(anim_folder)
            self.animations[anim_folder] = {}
            self.animations[anim_folder]["frames"] = []
            frames = os.path.join(ROOT, CHARACTERS_FOLDER, self.character_name, anim_folder)
            for frame in os.listdir(frames):
                self.animations[anim_folder]["frames"].append(frame)
            


class Characters:
    def __init__(self):
        self.characters = []
        self.load_characters()

    def load_characters(self):
        chars = os.path.join(ROOT, CHARACTERS_FOLDER)
        for character_name in os.listdir(chars):
            Character = CHARACATER(character_name)
            self.characters.append(Character)
