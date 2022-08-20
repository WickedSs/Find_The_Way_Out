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
        self.player = Player(self.character.characters[0], 1, 4)
        self.setup_group_sprites()

    def setup_group_sprites(self):
        self.players_group = pygame.sprite.Group()
        self.tiles_group = self.level.level_sprites
    
    def run(self):
        self.players_group.add(self.player)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)
            self.players_group.draw(self.screen)
            self.players_group.update(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
    