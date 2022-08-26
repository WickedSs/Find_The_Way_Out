import os, sys, pickle, pygame
from Core.Characters import Characters
from Overlay import Overlay
from Settings import *
from Core.Level import *
from Entities.Player import *
from Client import Network



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.overlay = Overlay()
        self.character = Characters()
        self.level = Level(self.overlay)
        self.player = Player(self.character.characters[0], self.overlay, 7.5 * SCALE_SIZE, 4 * SCALE_SIZE)
        # self.network = Network()
        # self.network_player = self.network.player
        # self.setup_player()
        self.setup_group_sprites()
        self.scroll = [0, 0]

    def setup_player(self):
        self.player = Player(self.character.characters[0], self.network_player.x, self.network_player.y)
        self.player.rect.width, self.player.rect.height = self.network_player.width, self.network_player.height
        self.player.selected_animation = self.network_player.selected_animation
        self.player.flipped = self.network_player.flipped
        self.player.playerID = self.network_player.player_id

    def setup_group_sprites(self):
        self.joined_players = []
        self.tiles_group = self.level.collision_group
    
    def update_other_player(self):
        PLAYERS_CONNECTED = self.network.send(self.network_player)
        players_ids = [player.playerID for player in self.joined_players]
        if PLAYERS_CONNECTED:
            for player_index in PLAYERS_CONNECTED:
                player_to_draw = PLAYERS_CONNECTED[player_index]
                if player_to_draw.player_id not in players_ids:
                    new_player = Player(self.character.characters[0], player_to_draw.x, player_to_draw.y)
                    new_player.playerID = player_to_draw.player_id
                    new_player.rect.width, new_player.rect.height = player_to_draw.width, player_to_draw.height
                    new_player.direction = pygame.math.Vector2(player_to_draw.direction)
                    new_player.selected_animation = player_to_draw.selected_animation
                    self.joined_players.append(new_player)
                else:
                    index = players_ids.index(player_to_draw.player_id)
                    player = self.joined_players[index]
                    player.direction = pygame.math.Vector2(player_to_draw.direction)
                    player.selected_animation = player_to_draw.selected_animation
                    

        if self.joined_players:
            _ = self.joined_players[0]
            # print(_.playerID.split("-")[0], _.selected_animation, self.player.playerID.split("-")[0], self.player.selected_animation, "---", self.network_player.selected_animation)
            print("Me: ", self.player.playerID.split("-")[0], self.player.direction[0], " - You: ", _.playerID.split("-")[0], _.direction[0])
            # print("[*]", _.selected_folder, _.selected_animation, _.direction)
                    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill("black")
            self.level.run(self.player)
            
            ## handle current player
            self.player.draw(self.screen)
            self.overlay.draw(self.player)
            
            self.player.update(self.tiles_group)
            self.overlay.update()
            
            # Draw Overlay
            # pygame.draw.rect(self.screen, (255, 255, 255), self.player.rect, 1)
            # self.network_player = self.player.player_update(self.network_player)

            ## handling other player
            # self.update_other_player()
            # for player in self.joined_players:
            #     player.draw(self.screen)
            #     player.update(self.tiles_group)

            # print("Rects: ", self.player.rect, [player.rect for player in self.joined_players])

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
    