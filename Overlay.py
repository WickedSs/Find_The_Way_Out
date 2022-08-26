import os, sys, pygame

from Settings import *

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
FONT_FILE = "Assets\Font\m6x11.ttf"

class Overlay:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay_surface.set_colorkey((0, 0, 0))
        self.overlay_surface.set_alpha(255)
        self.overlay_surface.fill((0, 0, 0))
        self.text_renderer = pygame.font.Font(os.path.join(ROOT, FONT_FILE), 25)
    
    def sliding_text(self):
        text_surface = self.text_renderer.render('Some Text', False, (255, 255, 255))
        self.overlay_surface.blit(text_surface, (0,0))
    
    def inventory_bar(self):
        width = (64 * 6) + (15 * 6)
        height = 70
        bottom_bar = pygame.Surface((width, height)).convert_alpha()
        bottom_bar.set_colorkey((0, 0, 0))
        bottom_bar.fill((0, 0, 0))
        bottom_bar.set_alpha(255)
        posX, posY = (SCREEN_WIDTH / 2) - (width / 2), SCREEN_HEIGHT - 90
        self.overlay_surface.blit(bottom_bar, (posX, posY))
                
    def draw(self):
        self.inventory_bar()
        self.sliding_text()
        self.display_surface.blit(self.overlay_surface, (10, 10))
