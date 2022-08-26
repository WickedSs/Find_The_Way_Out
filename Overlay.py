import os, sys, pygame

from Settings import *

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
FONT_FILE = "Assets\Font\m6x11.ttf"
GUI_FOLDER = "Assets\GUI"


ITEMS_IDENTIFIERS = {
    
}


class BOTTOM_BAR_SLOT:
    def __init__(self, x, y, image):
        self.item_identifier = 0
        self.x, self.y = x, y
        self.item = image
        self.item = pygame.transform.scale(self.item, (SCALE_SIZE, SCALE_SIZE))
        self.rect = self.item.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.amount = 0


class Overlay:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay_surface.set_colorkey((0, 0, 0))
        self.overlay_surface.set_alpha(255)
        self.overlay_surface.fill((0, 0, 0))
        self.text_renderer = pygame.font.Font(os.path.join(ROOT, FONT_FILE), 32)
        
        # Bottom_bar
        self.bottom_bar_path = os.path.join(ROOT, GUI_FOLDER, "Prefabs", "7.png")
        self.slide_text_surface = None

        # Booleans
        self.trigger_sliding_text = False
        self.text_to_slide = "DEFAULT"

        # Bottom Bar
        self.bottom_bar_width, self.bottom_bar_height = (64 * 6) + (15 * 6), 70
        # self.bottom_bar = pygame.Surface((self.bottom_bar_width, self.bottom_bar_height), pygame.SRCALPHA).convert_alpha()
        # self.bottom_bar.set_colorkey((0, 0, 0))
        # self.bottom_bar.fill((0, 0, 0))
        # self.bottom_bar.set_alpha(255)
        
    
    def sliding_text(self):
        
        if self.trigger_sliding_text:
            self.slinding_text_rect.x += 20
            if self.slinding_text_rect.x >= 10:
                self.trigger_sliding_text = False
                self.slinding_text_rect.x = 10
        
        if self.slide_text_surface:    
            self.overlay_surface.blit(self.slide_text_surface, self.slinding_text_rect)
                
            
            
    def inventory_bar(self):
        current_slot_x, current_slot_y = (SCREEN_WIDTH / 2) - (self.bottom_bar_width / 2), SCREEN_HEIGHT - 85
        for i in range(6):
            slot_image = pygame.image.load(self.bottom_bar_path)
            slot = BOTTOM_BAR_SLOT(current_slot_x, current_slot_y, slot_image)
            self.overlay_surface.blit(slot.item, slot.rect)
            current_slot_x += slot.rect.width + 10
            
        # self.overlay_surface.blit(self.bottom_bar, (posX, posY))

    def set_text_to_slide(self, text):
        self.text_to_slide = text
        self.slide_text_surface = self.text_renderer.render(self.text_to_slide, False, (255, 255, 255))
        self.slinding_text_rect = self.slide_text_surface.get_rect()
        self.slinding_text_rect.x, self.slinding_text_rect.y = -100, 100

    def draw(self):
        self.inventory_bar()
        self.display_surface.blit(self.overlay_surface, (10, 10))
        
    def update(self):
        
        # clear surface
        self.overlay_surface.set_colorkey((0, 0, 0))
        self.overlay_surface.set_alpha(255)
        self.overlay_surface.fill((0, 0, 0))
        
        self.sliding_text()
