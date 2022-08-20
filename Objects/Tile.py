
import pygame
from Settings import *



class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x * TILE_SIZE, self.y * TILE_SIZE
    

class Tile_WFC:
    def __init__(self, x, y, image):
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x * TILE_SIZE, self.y * TILE_SIZE
        self.up, self.right, self.down, self.left = [], [], [], [] 

    def rotate(self, angle):
        new_image = pygame.transform.rotate(self.image, 90 * angle)
        new_edges = [None for i in self.edges]
        length = len(self.edges);
        for i in range(length):
            new_edges[i] = self.edges[(i - angle + length) % length];
        return Tile(self.x, self.y, new_image, new_edges)
    
    def flip(self, x_axis, y_axis):
        new_image = pygame.transform.flip(self.image, x_axis, y_axis)
        new_edges = self.edges

        # horizontal axis flipping
        if x_axis:
            # process left edges
            edges_left, edge_right = new_edges[3].split(","), new_edges[1].split(",")
            for cardinal in range(len(edges_left)):
                edges_left[cardinal] = edges_left[cardinal][::-1]            
            new_edges[3] = ",".join(input for input in edges_left)
            
            # process right edges
            for cardinal in range(len(edge_right)):
                edge_right[cardinal] = edge_right[cardinal][::-1]
            new_edges[1] = ",".join(input for input in edge_right)
            
            # set the new edges
            new_edges[3], new_edges[1] = new_edges[1], new_edges[3]
            new_edges[0], new_edges[2] = new_edges[0][::-1], new_edges[2][::-1]
        
        # vertical axis flipping
        if y_axis:
            # process up edges
            edges_up, edges_down = new_edges[0].split(","), new_edges[2].split(",")        
            for cardinal in range(len(edges_up)):
                edges_up[cardinal] = edges_up[cardinal].strip()[::-1]
     
            new_edges[0] = ",".join(input for input in edges_up)

            # process down edges
            for cardinal in range(len(edges_down)):
                edges_down[cardinal] = edges_down[cardinal].strip()[::-1]
            
            new_edges[2] = ",".join(input for input in edges_down)
            
            # set the new edges
            new_edges[0], new_edges[2] = new_edges[2], new_edges[0]
            new_edges[3], new_edges[1] = new_edges[3][::-1], new_edges[1][::-1]
            
        return Tile(self.x, self.y, new_image, new_edges)