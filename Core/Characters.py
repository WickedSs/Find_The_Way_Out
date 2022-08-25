from fileinput import filename
from Settings import *
import os, sys
from PIL import Image
import numpy as np

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
CHARACTERS_FOLDER = "Assets\Characters"


class CHARACATER:
    def __init__(self, name):
        self.character_name = name
        self.animations = {}
        self.animations_folders = []
        self.load_animation()

    def crop_images(self, folder):
        for frame in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, frame)):
                current_frame = frame.split(".")
                if not os.path.exists(os.path.join(folder, "cropped", current_frame[0] + "-cropped.png")):
                    print(current_frame[0], "not cropped!")
                    loaded_image = Image.open(os.path.join(folder, frame))
                    loaded_image.load()
                    self.check_row(loaded_image, folder, current_frame[0])
                    
        return
    
    def check_row(self, image, folder, name):
        image_data = np.asarray(image)
        image_data_bw = image_data.max(axis=2)
        non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
        non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
        cropBox = (min(non_empty_rows), len(image_data), min(non_empty_columns), max(non_empty_columns))
        image_data_new = image_data[cropBox[0]:cropBox[1], cropBox[2]:cropBox[3]+1 , :]
        new_image = Image.fromarray(image_data_new)
        new_image.save(os.path.join(folder, "cropped", name + '-cropped.png'))
        print(cropBox)

    def load_animation(self):
        path = os.path.join(ROOT, CHARACTERS_FOLDER, self.character_name)
        for anim_folder in os.listdir(path):
            self.animations_folders.append(anim_folder)
            self.animations[anim_folder] = {}
            self.animations[anim_folder]["frames"] = []
            frames = os.path.join(ROOT, CHARACTERS_FOLDER, self.character_name, anim_folder, "cropped")
            # self.crop_images(frames)
            for frame in os.listdir(frames):
                if os.path.isfile(os.path.join(frames, frame)):
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
