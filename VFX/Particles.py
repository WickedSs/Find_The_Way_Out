from genericpath import isfile
import os, sys



ROOT = os.path.dirname(sys.modules['__main__'].__file__)
PARTICLES_FOLDER = "Assets\Particles"

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