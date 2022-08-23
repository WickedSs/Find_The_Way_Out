import pygame
import os, sys
from Characters import Characters
from Settings import *
from Level import *
from Objects.Player import *



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.character = Characters()
        self.player = Player(self.character.characters[0], 2, 3)
        self.setup_group_sprites()

    def setup_group_sprites(self):
        self.players_group = pygame.sprite.Group()
        self.tiles_group = self.level.collision_group
    
    def run(self):
        self.players_group.add(self.player)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # for sprite in self.tiles_group:
            #     offset_x, offset_y = (self.player.rect.x - sprite.rect.x), (self.player.rect.y - sprite.rect.y)
            #     if self.player.mask.overlap(sprite.mask, (offset_x, offset_y)):
            #         print("Grounded")
            #         self.player.grounded = True
            #     else:
            #         print("Not Grounded")
            #         self.player.grounded = False
            

            self.screen.fill("black")
            self.level.run()
            self.players_group.draw(self.screen)
            self.players_group.update(self.tiles_group)
            # for sprite in self.tiles_group.sprites():
            #     pygame.draw.rect(self.screen, (255, 255, 255), sprite.rect, 1)
            
            pygame.draw.rect(self.screen, (255, 255, 255), self.player.rect, 1)
            pygame.draw.rect(self.screen, (255, 255, 255), self.player.hitbox, 1)
            # pygame.draw.rect(self.screen, (255, 162, 255), self.player.up_hitbox, 2)
            # pygame.draw.rect(self.screen, (255, 162, 255), self.player.right_hitbox, 2)
            # pygame.draw.rect(self.screen, (255, 162, 255), self.player.down_hitbox, 2)
            # pygame.draw.rect(self.screen, (255, 162, 255), self.player.left_hitbox, 2)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
    