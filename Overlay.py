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
        self.health_bar_inner = "1.png"
        self.mana_bar_files = ["1.png", "4.png", "5.png"]
        self.mana_bar_inner = "2.png"

        # Sliding text
        self.slide_text_surface = None
        self.trigger_sliding_text = False
        self.slide_fade_out = 255
        self.start_tickes = -1
        self.text_to_slide = "DEFAULT"
        
        
        # floating text
        self.floating_text_distance_max = 5
        self.floating_text_distance = 0
        self.add_number = 0.25
        
        # Bottom Bar
        self.slots = 4
        self.bottom_bar_width, self.bottom_bar_height = (64 * self.slots) + (15 * 6), 70
        
    
    def draw_text(self, text, posx, posy):
        self.floating_text = self.text_renderer_24.render(text, False, (255, 255, 255))
        self.floating_text_rect = self.floating_text.get_rect()
        self.floating_text_rect.x, self.floating_text_rect.y = posx, posy
        
        self.floating_text_distance += self.add_number
        if self.floating_text_distance >= 8:
            self.add_number = -0.35
        elif self.floating_text_distance <= 0:
            self.add_number = 0.35
        
        self.floating_text_rect.y += self.floating_text_distance
        self.display_surface.blit(self.floating_text, self.floating_text_rect)
    
    def sliding_text(self):
        if self.trigger_sliding_text:
            self.slinding_text_rect.x += 20
            if self.slinding_text_rect.x >= 10:
                self.slinding_text_rect.x = 10
                self.trigger_sliding_text = False
                self.start_tickes = pygame.time.get_ticks()
        
        if self.slide_text_surface:    
            self.overlay_surface.blit(self.slide_text_surface, self.slinding_text_rect)
            
        self.hide_sliding_text()
            
    def hide_sliding_text(self):
        if self.start_tickes != -1:
            if (pygame.time.get_ticks() - self.start_tickes) / 1000 >= 3:
                self.slide_text_surface.set_alpha(self.slide_fade_out)
                self.slide_fade_out -= 30
            
            if self.slide_fade_out == 0:
                self.slinding_text_rect.x = -100
                self.slide_fade_out = 255
                self.trigger_sliding_text = False
                self.start_tickes = -1
                self.slide_text_surface = None

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

        self.heath_bar_inner_pos = pygame.math.Vector2(45, SCREEN_HEIGHT - 86)
        self.inner_bar_red = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, "Life_Bars\Colors", self.health_bar_inner)).convert_alpha()
        # current_health = (player * (self.inner_bar_red_rect.x * 4.8)) / 100
        # self.inner_bar_red = pygame.transform.scale(self.inner_bar_red, (current_health, 4))
        # self.inner_bar_red_rect = image.get_rect()
        # self.inner_bar_red_rect.x, self.inner_bar_red_rect.y = heath_bar_inner_pos.x, heath_bar_inner_pos.y
        self.increase_health_bar(player)
        self.overlay_surface.blit(self.inner_bar_red, self.inner_bar_red_rect)

        
        heath_bar_pos = pygame.math.Vector2(12.5, SCREEN_HEIGHT - 60)
        for pic in self.mana_bar_files:
            image = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, "Life_Bars\Medium_Bars", pic)).convert_alpha()
            image_rect = image.get_rect()
            image = pygame.transform.scale(image, (image_rect.w * 2, image_rect.height * 2))
            image_rect = image.get_rect()
            image_rect.x, image_rect.y = heath_bar_pos.x, heath_bar_pos.y
            self.overlay_surface.blit(image, image_rect)
            heath_bar_pos.x += image_rect.width

        self.mana_bar_inner_pos = pygame.math.Vector2(40, SCREEN_HEIGHT - 46)
        self.inner_bar_blue = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, "Life_Bars\Colors", self.mana_bar_inner)).convert_alpha()
        # self.inner_bar_blue_rect = self.inner_bar_blue.get_rect()
        # self.inner_bar_blue = pygame.transform.scale(self.inner_bar_blue, (self.inner_bar_blue_rect.w, 4))
        # self.inner_bar_blue_rect = image.get_rect()
        # self.inner_bar_blue_rect.x, self.inner_bar_blue_rect.y = self.mana_bar_inner_pos.x, self.mana_bar_inner_pos.y
        self.increase_mana_bar(player)
        self.overlay_surface.blit(self.inner_bar_blue, self.inner_bar_blue_rect)
                
        self.overlay_surface.blit(self.player_frame_image, self.player_frame_rect)
        self.overlay_surface.blit(self.player_name, self.player_name_rect)
        self.overlay_surface.blit(self.maps_text, self.maps_text_rect)
        self.overlay_surface.blit(self.maps_holded, self.maps_holded_rect)
        self.overlay_surface.blit(player.player_portrait, self.player_portrait_rect)
        # pygame.draw.rect(self.overlay_surface, (255, 255, 255), self.player_portrait_rect, 1)
    
    def increase_health_bar(self, player):
        if player.health <= player.max_health:
            self.inner_bar_red_rect = self.inner_bar_red.get_rect()
            current_health = (player.health * (self.inner_bar_red_rect.w * 4.8)) / player.max_health
            self.inner_bar_red = pygame.transform.scale(self.inner_bar_red, (current_health, 4))
            player.health += 0.08
        else:
            current_health = 32 * 4.8
            self.inner_bar_red = pygame.transform.scale(self.inner_bar_red, (current_health, 4))

        self.inner_bar_red_rect = self.inner_bar_red.get_rect()
        self.inner_bar_red_rect.x, self.inner_bar_red_rect.y = self.heath_bar_inner_pos.x, self.heath_bar_inner_pos.y

    def increase_mana_bar(self, player):
        if player.mana <= player.max_mana:
            self.inner_bar_blue_rect = self.inner_bar_blue.get_rect()
            current_mana = (player.mana * (self.inner_bar_blue_rect.w * 3.2)) / player.max_mana
            self.inner_bar_blue = pygame.transform.scale(self.inner_bar_blue, (current_mana, 4))
            player.mana += 0.25
        else:
            current_mana = 32 * 3.2
            self.inner_bar_blue = pygame.transform.scale(self.inner_bar_blue, (current_mana, 4))

        self.inner_bar_blue_rect = self.inner_bar_blue.get_rect()
        self.inner_bar_blue_rect.x, self.inner_bar_blue_rect.y = self.mana_bar_inner_pos.x, self.mana_bar_inner_pos.y

    def inventory_bar(self):
        current_slot_x, current_slot_y = (SCREEN_WIDTH / 2) - (self.bottom_bar_width / 2), SCREEN_HEIGHT - 85
        for i in range(self.slots):
            slot_image = pygame.image.load(self.bottom_bar_path)
            slot = BOTTOM_BAR_SLOT(current_slot_x, current_slot_y, slot_image)
            self.overlay_surface.blit(slot.item, slot.rect)
            current_slot_x += slot.rect.width + 10
            

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
