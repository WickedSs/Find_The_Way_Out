import os, sys


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
ITEMS_FOLDER = "Assets\Particles"



class Item:
    
    def animate(self):
        return


class Big_Map(Item):
    
    def __init__(self):
        self.animations = {}
        self.animation_names = []
        self.animate()
        
    

class Blue_Diamond(Item):
    def __init__(self):
        pass


class Blue_Potion(Item):
    def __init__(self):
        pass


class Gold_Coin(Item):
    def __init__(self):
        pass


class Silver_Coin(Item):
    def __init__(self):
        pass

    
class Golden_Skull(Item):
    def __init__(self):
        pass


class Green_Bottle(Item):
    def __init__(self):
        pass


class Green_Diamond(Item):
    def __init__(self):
        pass


class Red_Diamond(Item):
    def __init__(self):
        pass
    

class Red_Postion(Item):
    def __init__(self):
        pass

