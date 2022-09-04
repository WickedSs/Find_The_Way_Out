import os, sys, pygame
from Entities.Item import Item



ROOT = os.path.dirname(sys.modules['__main__'].__file__)
PARTICLES_FOLDER = "Assets\Particles"


class Particle:
    def __init__(self):
        pass


class Big_Map_particle(Item):
    def __init__(self, status, width, height):
        super().__init__(width, height, True, True, None, 0, 0)
        self.display_surface = pygame.display.get_surface()
        self.asset_name = "Map_Effect"
        self.animation_type = "Multiple"
        self.status = status
        self.path = os.path.join(PARTICLES_FOLDER, self.asset_name)
        self.status_path = os.path.join(self.path, self.status)
        self.multiple_animations()
        self.working_animation = self.animations[status]
        
    def play_animation_once(self):
        self.animation_index += 0.12
        if self.animation_index >= len(self.working_animation):
            self.animation_index = 0
            return True
        
        self.get_frame()
        self.update(0, 0)
        self.draw()
        return False
    

class Ball_Explosion(Item):
    def __init__(self, status, width, height):
        super().__init__(width, height, True, True, None, 0, 0, 4, 4)
        self.display_surface = pygame.display.get_surface()
        self.asset_name = "Ball_Explosion"
        self.animation_type = "Single"
        self.status = status
        self.path = os.path.join(PARTICLES_FOLDER, self.asset_name)
        self.status_path = os.path.join(self.path, self.status)
        self.multiple_animations()
        self.play = False
        self.working_animation = self.animations[status]
        
    def play_animation_once(self):
        if self.play:
            self.animation_index += 0.12
            if self.animation_index >= len(self.working_animation):
                self.animation_index = 0
                self.kill()
                return
            
            self.get_frame()
            self.update(0, 0)
            self.draw()

class Particles:
    def __init__(self, character):
        self.character = character
        self.particles = {}
        self.particle_folders = []
        self.load_particles()


    def load_particles(self):
        particles_path = os.path.join(PARTICLES_FOLDER, self.character)
        for folder in os.listdir(particles_path):
            self.particles[folder] = {}
            self.particles[folder]["frames"] = []
            frames_path = os.path.join(PARTICLES_FOLDER, self.character, folder)
            self.particle_folders.append(folder)
            for frame in os.listdir(frames_path):
                if os.path.isfile(os.path.join(frames_path, frame)):
                    self.particles[folder]["frames"].append(frame)