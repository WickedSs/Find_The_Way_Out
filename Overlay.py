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
        
        # Booleans
        self.trigger_sliding_text = True
        self.text_to_slide = "DEFAULT"
        
        # Sliding Text
        self.text_surface = self.text_renderer.render(self.text_to_slide, False, (255, 255, 255))
        self.slinding_text_rect = self.text_surface.get_rect()
        self.slinding_text_rect.x, self.slinding_text_rect.y = -100, 100
        
    
    def sliding_text(self):
        
        if self.trigger_sliding_text:
            self.slinding_text_rect.x += 5
            print(self.slinding_text_rect, self.trigger_sliding_text)
            if self.slinding_text_rect.x == 10:
                self.trigger_sliding_text = False
                self.slinding_text_rect.x, self.slinding_text_rect.y = -100, 100
                
            
            
    def inventory_bar(self):
        width = (64 * 6) + (15 * 6)
        height = 70
        bottom_bar = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        bottom_bar.set_colorkey((0, 0, 0))
        bottom_bar.fill((0, 0, 0))
        bottom_bar.set_alpha(128)
        posX, posY = (SCREEN_WIDTH / 2) - (width / 2), SCREEN_HEIGHT - 85
        
        current_slot_x, current_slot_y = 0, 0
        for i in range(6):
            slot_image = pygame.image.load(self.bottom_bar_path)
            slot = BOTTOM_BAR_SLOT(current_slot_x, current_slot_y, slot_image)
            bottom_bar.blit(slot.item, slot.rect)
            current_slot_x += slot.rect.width + 10
            
        self.overlay_surface.blit(bottom_bar, (posX, posY))
                
    def draw(self):
        self.inventory_bar()
        self.overlay_surface.blit(self.text_surface, self.slinding_text_rect)
        self.display_surface.blit(self.overlay_surface, (10, 10))
        
    def update(self):
        
        # clear surface
        self.overlay_surface.set_colorkey((0, 0, 0))
        self.overlay_surface.set_alpha(255)
        self.overlay_surface.fill((0, 0, 0))
        
        
        self.sliding_text()
