import os, sys


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
ITEMS_FOLDER = "Assets\Items"

class Items:
    def __init__(self):
        self.items = {}
        self.big_map = {
            "Idle" : [],
            "Folding" : [],
            "Unfolding" : []
        }
        self.particle_folders = []
        self.load_items()
    
    def load_items(self):
        items_path = os.path.join(ITEMS_FOLDER)
        for folder in os.listdir(items_path):
            if folder != "Big_Map":
                self.items[folder] = {}
                self.items[folder]["frames"] = []
                frames_path = os.path.join(ITEMS_FOLDER, folder)
                self.particle_folders.append(folder)
                for frame in os.listdir(frames_path):
                    if os.path.isfile(os.path.join(frames_path, frame)):
                        self.items[folder]["frames"].append(frame)
            else:
                frames_path = os.path.join(ITEMS_FOLDER, folder)
                for inner_folder in os.listdir(frames_path):
                    for frame in os.listdir(os.path.join(frames_path, inner_folder)):
                        self.big_map[inner_folder].append(frame)