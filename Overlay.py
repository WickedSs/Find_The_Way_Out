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
        
        self.text_renderer_20 = pygame.font.Font(os.path.join(ROOT, FONT_FILE), 20)
        self.text_renderer_24 = pygame.font.Font(os.path.join(ROOT, FONT_FILE), 24)
        self.text_renderer_32 = pygame.font.Font(os.path.join(ROOT, FONT_FILE), 16)
        
        # Bottom_bar
        self.bottom_bar_path = os.path.join(ROOT, GUI_FOLDER, "Prefabs", "7.png")
        self.player_frame = os.path.join(ROOT, GUI_FOLDER, "Prefabs", "13.png")
        self.health_bar_files = ["1.png", "3.png", "4.png"]
        self.mana_bar_files = ["1.png", "4.png", "5.png"]

        # Sliding text
        self.slide_text_surface = None
        self.trigger_sliding_text = False
        self.slide_fade_out = 255
        self.start_tickes = -1
        self.text_to_slide = "DEFAULT"

        # Bottom Bar
        self.slots = 3
        self.bottom_bar_width, self.bottom_bar_height = (64 * self.slots) + (15 * 6), 70
        
    
    def sliding_text(self):
        if self.trigger_sliding_text:
            self.slinding_text_rect.x += 20
            if self.slinding_text_rect.x >= 10:
                self.slinding_text_rect.x = 10
                self.start_tickes = pygame.time.get_ticks()
        
        if self.slide_text_surface:    
            self.overlay_surface.blit(self.slide_text_surface, self.slinding_text_rect)
            
        self.hide_sliding_text()
        
            
    def hide_sliding_text(self):
        print(self.trigger_sliding_text, self.start_tickes)
        if self.trigger_sliding_text and self.start_tickes != -1:
            if (pygame.time.get_ticks() - self.start_tickes) / 1000 == 5:
                self.slide_text_surface.set_alpha(self.slide_fade_out)
            
            if self.slide_fade_out == 0:
                self.slinding_text_rect.x = -100
                self.slide_fade_out = 255
                self.trigger_sliding_text = False
                
    def player_data(self, player):
        self.player_frame_image = pygame.image.load(self.player_frame)
        self.player_frame_rect = self.player_frame_image.get_rect()
        self.player_frame_rect.x, self.player_frame_rect.y = 0, 0
        
        self.player_portrait_rect = player.player_portrait.get_rect()
        self.player_portrait_rect.x, self.player_portrait_rect.y = 12.5, 10
        
        self.player_name = self.text_renderer_20.render(player.player_name, False, (255, 255, 255))
        self.player_name_rect = self.player_name.get_rect()
        self.player_name_rect.x, self.player_name_rect.y = self.player_frame_rect.right + 5, 5
        
        self.maps_text = self.text_renderer_20.render("Maps ", False, (255, 255, 255))
        self.maps_text_rect = self.maps_text.get_rect()
        self.maps_text_rect.x, self.maps_text_rect.y = self.player_frame_rect.right + 5, self.player_frame_rect.top + 30 
        
        self.maps_holded = self.text_renderer_20.render("x" + str(player.collected_maps), False, (0, 255, 0))
        self.maps_holded_rect = self.maps_holded.get_rect()
        self.maps_holded_rect.x, self.maps_holded_rect.y = self.maps_text_rect.right, self.player_frame_rect.top + 30
        
        heath_bar_pos = pygame.math.Vector2(12.5, SCREEN_HEIGHT - 100)
        for pic in self.health_bar_files:
            image = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, "Life_Bars\Big_Bars", pic)).convert_alpha()
            image_rect = image.get_rect()
            image = pygame.transform.scale(image, (image_rect.w * 2, image_rect.height * 2))
            image_rect = image.get_rect()
            image_rect.x, image_rect.y = heath_bar_pos.x, heath_bar_pos.y
            self.overlay_surface.blit(image, image_rect)
            heath_bar_pos.x += image_rect.width
        
        heath_bar_pos = pygame.math.Vector2(12.5, SCREEN_HEIGHT - 60)
        for pic in self.mana_bar_files:
            image = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, "Life_Bars\Medium_Bars", pic)).convert_alpha()
            image_rect = image.get_rect()
            image = pygame.transform.scale(image, (image_rect.w * 2, image_rect.height * 2))
            image_rect = image.get_rect()
            image_rect.x, image_rect.y = heath_bar_pos.x, heath_bar_pos.y
            self.overlay_surface.blit(image, image_rect)
            heath_bar_pos.x += image_rect.width 
            
        
        self.overlay_surface.blit(self.player_frame_image, self.player_frame_rect)
        self.overlay_surface.blit(self.player_name, self.player_name_rect)
        self.overlay_surface.blit(self.maps_text, self.maps_text_rect)
        self.overlay_surface.blit(self.maps_holded, self.maps_holded_rect)
        self.overlay_surface.blit(player.player_portrait, self.player_portrait_rect)
        # pygame.draw.rect(self.overlay_surface, (255, 255, 255), self.player_portrait_rect, 1)
        
    def inventory_bar(self):
        current_slot_x, current_slot_y = (SCREEN_WIDTH / 2) - (self.bottom_bar_width / 2), SCREEN_HEIGHT - 85
        for i in range(self.slots):
            slot_image = pygame.image.load(self.bottom_bar_path)
            slot = BOTTOM_BAR_SLOT(current_slot_x, current_slot_y, slot_image)
            self.overlay_surface.blit(slot.item, slot.rect)
            current_slot_x += slot.rect.width + 10
            
        # self.overlay_surface.blit(self.bottom_bar, (posX, posY))

    def set_text_to_slide(self, text):
        self.text_to_slide = text
        self.slide_text_surface = self.text_renderer_24.render(self.text_to_slide, False, (255, 255, 255))
        self.slinding_text_rect = self.slide_text_surface.get_rect()
        self.slinding_text_rect.x, self.slinding_text_rect.y = -100, 100

    def draw(self, player):
        self.inventory_bar()
        self.player_data(player)
        self.display_surface.blit(self.overlay_surface, (10, 10))
        
    def update(self):
        
        # clear surface
        self.overlay_surface.set_colorkey((0, 0, 0))
        self.overlay_surface.set_alpha(255)
        self.overlay_surface.fill((0, 0, 0))
        
        self.sliding_text()
