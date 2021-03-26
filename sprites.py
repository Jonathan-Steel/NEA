import pygame
import random
import xml.etree.ElementTree as ET
import numpy as np
import math

from library import *
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.spritesheet = load_spritesheet('assets/original/Spritesheets/spritesheet_vehicles.png', 'assets/original/Spritesheets/spritesheet_vehicles.xml')
        self.image = self.spritesheet[3]
        self.rect = self.image.get_rect()

        self.s = np.array([[WIDTH/4], [HEIGHT/2]])
        self.v = np.array([[0.0], [0.0]])
        self.const_a = ((DRIVING_FORCE - FRICTIONAL_FORCE) / CAR_MASS)
        self.a = np.array([[0.0], [0.0]])
        self.rect.center = (int(self.s[0]), int(self.s[1]))

    def update(self):
        self.v += self.a
        self.s += self.v

        self.rect.center = (int(self.s[0]), int(self.s[1]))

    def accelerate(self, theta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # This won't work use np.matmul(a_transform, a)
            self.a = self.const_a * (np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]]) * np.array([[1.0], [1.0]]))
            print(self.a)
        else:
            self.a *= 0
            

# player = Player('')

# print(player.s)