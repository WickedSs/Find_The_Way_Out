import os, sys, pickle, pygame
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
        # self.player = Player(self.character.characters[0], random.randrange(2, 6) * SCALE_SIZE, random.randrange(3, 5) * SCALE_SIZE)
        self.network = Network()
        self.networkPlayer = self.network.player
        self.setup_player()
        self.setup_group_sprites()

    def setup_player(self):
        self.player = Player(self.character.characters[0], self.networkPlayer.x, self.networkPlayer.y)
        self.player.rect.width, self.player.rect.height = self.networkPlayer.width, self.networkPlayer.height
        self.player.selected_folder = self.animations_names[self.networkPlayer.anim_folder]
        self.player.flipped = self.networkPlayer.flipped
        self.player.playerID = self.networkPlayer.player_id

    def setup_group_sprites(self):
        self.joined_players = []
        self.joined_ids = []
        self.tiles_group = self.level.collision_group
    
    def update_other_player(self):
        PLAYERS_CONNECTED = self.network.send(self.network_player)
        print("Players: ", PLAYERS_CONNECTED, len(PLAYERS_CONNECTED))
        if PLAYERS_CONNECTED:
            for player_index in PLAYERS_CONNECTED:
                player_to_draw = PLAYERS_CONNECTED[player_index]
                new_player = Player(self.character.characters[0], player_to_draw.rect[0], player_to_draw.rect[1])
                new_player.rect.width, new_player.rect.height = player_to_draw.rect[2], player_to_draw.rect[3]
                new_player.selected_folder = player_to_draw.anim_folder
                new_player.flipped = player_to_draw.flipped
                new_player.playerID = player_to_draw.player_id
                new_player.draw(self.screen)
                new_player.update(self.tiles_group)

            
                    

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

            # print("Rects: ", self.player.rect, [player.rect for player in self.joined_players])

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
    