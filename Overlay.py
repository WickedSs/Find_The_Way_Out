import os, sys, pygame, random
from Settings import *
from Entities.Item import *

ROOT = os.path.dirname(sys.modules['__main__'].__file__)
FONT_FILE = "Assets\Font\m6x11.ttf"
GUI_FOLDER = "Assets\GUI"
ITEMS_FOLDER = "Assets\Items"


ITEMS_IDENTIFIERS = {
    
}


class BOTTOM_BAR_SLOT(pygame.sprite.Sprite):
    def __init__(self, x, y, background, item, text_render):
        self.item_identifier = 0
        self.x, self.y = x, y
        self.text_render = text_render
        
        self.background = background
        self.rect_background = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (self.rect_background.w * 2, self.rect_background.h * 2))
        self.rect_background = self.background.get_rect()
        self.rect_background.x, self.rect_background.y = self.x, self.y
        
        self.item = item
        self.rect_item = self.item.get_rect()
        self.item = pygame.transform.scale(self.item, (self.rect_item.w * 3, self.rect_item.h * 3))
        self.rect_item = self.item.get_rect()
        self.rect_item.x, self.rect_item.y = self.rect_background.x + self.rect_background.w / 3, self.rect_background.y + self.rect_background.h / 5
        
        self.amount = 5
        self.amount_text = self.text_render.render(str(self.amount), False, (0, 0, 0))
        self.amount_rect = self.amount_text.get_rect()
        self.amount_rect.x, self.amount_rect.y = self.rect_background.x + self.rect_background.w - 15, self.rect_background.y + self.rect_background.h - 25

        
    def update(self):
        return
    
    def draw(self, screen):
        screen.blit(self.background, self.rect_background)
        screen.blit(self.item, self.rect_item)
        screen.blit(self.amount_text, self.amount_rect)


class Overlay:
    def __init__(self, clock):
        self.clock = clock
        self.display_surface = pygame.display.get_surface()
        self.overlay_group = pygame.sprite.Group()
        self.overlay_bars_group = pygame.sprite.Group()
        
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        self.overlay_surface.set_colorkey((0, 0, 0))
        self.overlay_surface.fill((0, 0, 0))
        
        # Bottom_bar
        self.slots = 3
        self.bottom_bar_width, self.bottom_bar_height = 124 + (48 * (self.slots - 2)), 90
        
        self.bottom_bar_path = ["Inventory", "10.png", "11.png", "12.png"]
        self.slide_text_background = ["Yellow_Paper", "10.png", "11.png", "12.png"]
        
        self.health_bar_files = ["Life_Bars\\Big_Bars", "1.png", "3.png", "4.png"]
        self.health_bar_inner = "Life_Bars\\Colors\\1.png"
        
        self.mana_bar_files = ["Life_Bars\\Medium_Bars", "1.png", "4.png", "5.png"]
        self.mana_bar_inner = "Life_Bars\\Colors\\2.png"

        # Sliding text
        self.slide_text_surface = None
        self.trigger_sliding_text = False
        self.slide_fade_out = 255
        self.start_tickes = -1
        self.text_to_slide = "DEFAULT"
        
        # transition screen
        self.current_alpha = self.overlay_surface.get_alpha()
        self.dim_screen_counter = 0
        self.dim_screen_bool = False
        self.trigger_fade_in = False
        
        # floating text
        self.floating_text_distance_max = 5
        self.floating_text_distance = 0
        self.floating_add_number = 0.25
                
    
    def set_font(self, size):
        return pygame.font.Font(os.path.join(ROOT, FONT_FILE), size)
    
    def initialize_overlay(self, player):
        self.bottom_inventory_bar()
        self.player_UI(player)
    
    def fade_out_screen(self):
        if self.dim_screen_counter <= SCREEN_WIDTH:
            self.dim_screen_counter += SCREEN_WIDTH / 20
        else:
            self.dim_screen_counter = SCREEN_WIDTH - 60
            pygame.time.delay(2000)
            self.trigger_fade_in = True
            self.dim_screen_bool = False
                        
        for i in range(0, 6, 2):
            pygame.draw.rect(self.display_surface, (51, 50, 61), (0, i * 100, self.dim_screen_counter, SCREEN_HEIGHT))
        
    def fade_in_screen(self):
        if self.dim_screen_counter > 0:
            self.dim_screen_counter -= SCREEN_WIDTH / 20
        else:
            self.dim_screen_counter = 0
            self.trigger_fade_in = False
            self.dim_screen_bool = False      
        
        for i in range(6, -1, -2):
            pygame.draw.rect(self.display_surface, (51, 50, 61), (0, i * 100, self.dim_screen_counter, SCREEN_HEIGHT))
          
    def draw_text(self, text, posx, posy):
        self.floating_text = self.set_font(24).render(text, False, (255, 255, 255))
        self.floating_text_rect = self.floating_text.get_rect()
        self.floating_text_rect.x, self.floating_text_rect.y = posx, posy
        
        self.floating_text_distance += self.floating_add_number
        if self.floating_text_distance >= 8:
            self.floating_add_number = -0.35
        elif self.floating_text_distance <= 0:
            self.floating_add_number = 0.35
        
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

    def player_UI(self, player):
        self.player_name = GUI_ITEM(10, 15, None, self.set_font(32), player.player_name)
        self.fps = GUI_ITEM(SCREEN_WIDTH / 2, 15, None, self.set_font(26), self.clock.get_fps())
        self.maps_text = GUI_ITEM(10, self.player_name.rect.top + 30, None, self.set_font(26), "Maps ")
        self.maps_holded = GUI_ITEM(self.maps_text.rect.right, self.player_name.rect.top + 30, None, self.set_font(26), "x" + str(player.collected_maps))
        
        heath_bar_pos = pygame.math.Vector2(12.5, SCREEN_HEIGHT - 80)
        for i in range(len(self.health_bar_files)-1):
            image = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, self.health_bar_files[0], self.health_bar_files[i+1])).convert_alpha()
            image_rect = image.get_rect()
            image = pygame.transform.scale(image, (image_rect.w * 2, image_rect.height * 2))
            image_rect = image.get_rect()
            image_rect.x, image_rect.y = heath_bar_pos.x, heath_bar_pos.y
            image_sprite = GUI_ITEM(heath_bar_pos.x, heath_bar_pos.y, image)
            self.overlay_group.add(image_sprite)
            
            heath_bar_pos.x += image_rect.width

        self.heath_bar_inner_pos = (45, SCREEN_HEIGHT - 66)
        self.inner_bar_red = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, self.health_bar_inner)).convert_alpha()
        self.inner_bar_red = pygame.transform.scale(self.inner_bar_red, (32 * 4.8, 4))
        self.inner_bar_red_rect = self.inner_bar_red.get_rect(topleft=self.heath_bar_inner_pos)
        
        
        # self.increase_health_bar(player)
        inner_bar_red = GUI_ITEM_BAR(self.inner_bar_red_rect.x, self.inner_bar_red_rect.y, self.inner_bar_red, "Health", player)
        self.overlay_bars_group.add(inner_bar_red)
        
        mana_bar_pos = pygame.math.Vector2(12.5, SCREEN_HEIGHT - 40)
        for i in range(len(self.mana_bar_files)-1):
            image = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, self.mana_bar_files[0], self.mana_bar_files[i+1])).convert_alpha()
            image_rect = image.get_rect()
            image = pygame.transform.scale(image, (image_rect.w * 2, image_rect.height * 2))
            image_rect = image.get_rect()
            image_rect.x, image_rect.y = mana_bar_pos.x, mana_bar_pos.y
            image_sprite = GUI_ITEM(mana_bar_pos.x, mana_bar_pos.y, image)
            self.overlay_group.add(image_sprite)
            mana_bar_pos.x += image_rect.width

        self.mana_bar_inner_pos = (40, SCREEN_HEIGHT - 26)
        self.inner_bar_blue = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, self.mana_bar_inner)).convert_alpha()
        self.inner_bar_blue = pygame.transform.scale(self.inner_bar_blue, (32 * 3.24, 4))
        self.inner_bar_blue_rect = self.inner_bar_blue.get_rect(topleft=self.mana_bar_inner_pos)
        inner_bar_blue = GUI_ITEM_BAR(self.inner_bar_blue_rect.x, self.inner_bar_blue_rect.y, self.inner_bar_blue, "Mana", player)
        self.overlay_bars_group.add(inner_bar_blue)
        
        self.overlay_group.add(self.player_name)
        self.overlay_group.add(self.maps_text)
        self.overlay_group.add(self.maps_holded)
        self.overlay_group.add(self.fps)

    def bottom_inventory_bar(self):
        self.slots_content = ["Red_Potion\\01.png", "Blue_Potion\\01.png", "Chest_Key\\1.png"]
        self.slots_offset = [0.1, 0.5, 0.8]
        current_slot_x, current_slot_y = (SCREEN_WIDTH - self.bottom_bar_width) / 2, SCREEN_HEIGHT - self.bottom_bar_height
        for i in range(self.slots):
            slot_background_image = pygame.image.load(os.path.join(ROOT, GUI_FOLDER, self.bottom_bar_path[0], self.bottom_bar_path[i+1]))
            slot_content = pygame.image.load(os.path.join(ROOT, ITEMS_FOLDER, self.slots_content[i]))
            slot_background_rect, slot_content_rect = slot_background_image.get_rect(), slot_content.get_rect()
            
            slot_background_image = pygame.transform.scale(slot_background_image, (slot_background_rect.w * 2, slot_background_rect.h * 2))
            slot_content = pygame.transform.scale(slot_content, (slot_content_rect.w * 2, slot_content_rect.h * 2))
            slot_background_rect, slot_content_rect = slot_background_image.get_rect(), slot_content.get_rect()
           
            current_slot_content_x = (current_slot_x + (slot_background_rect.width / 2)) -  (slot_content_rect.width * self.slots_offset[i]) 
            current_slot_content_y = (current_slot_y + (slot_background_rect.height / 2)) - (slot_content_rect.height / 2)
            
            slot_sprite = GUI_ITEM(current_slot_x, current_slot_y, slot_background_image)
            slot_content_sprite = GUI_ITEM(current_slot_content_x, current_slot_content_y, slot_content)

            current_slot_x += slot_background_rect.width
            self.overlay_group.add(slot_sprite)
            self.overlay_group.add(slot_content_sprite)
            
    def set_text_to_slide(self, text):
        self.text_to_slide = text
        self.slide_text_surface = self.text_renderer_24.render(self.text_to_slide, False, (255, 255, 255))
        self.slinding_text_rect = self.slide_text_surface.get_rect()
        self.slinding_text_rect.x, self.slinding_text_rect.y = -100, 100

    def draw(self, player):
        return
        
    def update(self, player):
        # pygame.draw.line(self.display_surface, (255, 255, 255), ((SCREEN_WIDTH / 2) - (self.bottom_bar_width / 2), 0), ((SCREEN_WIDTH / 2) - (self.bottom_bar_width / 2), SCREEN_HEIGHT), 1)
        # pygame.draw.line(self.display_surface, (255, 255, 255), ((SCREEN_WIDTH / 2) + (self.bottom_bar_width / 2), 0), ((SCREEN_WIDTH / 2) + (self.bottom_bar_width / 2), SCREEN_HEIGHT), 1)
        self.fps.set_text(int(self.clock.get_fps()))
        if not self.dim_screen_bool and not self.trigger_fade_in:
            self.overlay_surface.fill((0, 0, 0))
        
        self.overlay_group.update(0, 0, player)
        self.overlay_group.draw(self.overlay_surface)
        
        self.overlay_bars_group.update()
        self.overlay_bars_group.draw(self.overlay_surface)
        self.display_surface.blit(self.overlay_surface, (0, 0))
        
        if self.dim_screen_bool: 
            self.fade_out_screen()
        
        if self.trigger_fade_in:
            self.fade_in_screen()
        
