from calendar import day_abbr
from re import A
import pygame
import os, sys
from Characters import Characters
from Settings import *
from Level import *
from Objects.Player import *
from Client import Network



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.character = Characters()
        self.player = Player(self.character.characters[0], random.randrange(2, 6) * SCALE_SIZE, random.randrange(3, 5) * SCALE_SIZE)
        self.network = Network(self.player)
        self.setup_group_sprites()

    def setup_group_sprites(self):
        self.joined_players = []
        self.joined_ids = []
        self.tiles_group = self.level.collision_group
    
    def update_other_player(self):
        player_position = "{0},{1},{2}".format(self.player.playerID, self.player.rect.x, self.player.rect.y)
        PLAYERS_CONNECTED = self.network.send(player_position.encode())
        players = PLAYERS_CONNECTED.split("|")
        players = [player for player in players if player != ""]
        print("Players: ", players, self.player.playerID)
        self.new_group = pygame.sprite.Group()
        if players:
            for player in players:
                data = player.split(",")
                if data[0] != self.player.playerID:
                    if data[0] not in self.joined_ids:
                        new_player = Player(self.character.characters[0], int(data[1]), int(data[2]))
                        new_player.set_playerID(data[0])
                        self.joined_ids.append(data[0])
                        self.joined_players.append(new_player)
                    else:
                        index = self.joined_ids.index(data[0])
                        self.working_player = self.joined_players[index]
                        self.working_player.rect.x, self.working_player.rect.y = int(data[1]), int(data[2])
                else:
                    pass

            
                    

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill("black")
            self.level.run()
            
            # handle current player
            self.player.draw(self.screen)
            self.player.update(self.tiles_group)

            # handling other player
            self.update_other_player()
            for player in self.joined_players:
                player.draw(self.screen)
                player.update(self.tiles_group)

            # print("Rects: ", self.player.rect, [player.rect for player in self.joined_players])

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
    