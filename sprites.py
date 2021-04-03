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
        # self.original_image = self.spritesheet[3]
        # self.image = pygame.transform.rotate(self.original_image, -90)
        self.original_image = pygame.transform.rotate(pygame.transform.scale(self.spritesheet[3], (self.spritesheet[3].get_width() // 2, self.spritesheet[3].get_height() // 2)), -90)
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.s = np.array([[WIDTH/4], [HEIGHT/2]])
        self.v = np.array([[0.0], [0.0]])
        self.const_a = 0
        self.a = np.array([[0.0], [0.0]])
        self.rect.center = (int(self.s[0]), int(self.s[1]))
        self.theta = 0

    def update(self):
        self.v_magnitude = np.linalg.norm(self.v)

        keys = pygame.key.get_pressed()

        delta_theta = 0
        if keys[pygame.K_a] and not(keys[pygame.K_d]):
            delta_theta = self.v_magnitude / 4
        if keys[pygame.K_d] and not(keys[pygame.K_a]):
            delta_theta = -(self.v_magnitude / 4)

        self.rotate(delta_theta)

        self.accelerate()

        if self.a[0] == 0 and self.a[1] == 0 and delta_theta != 0:
            self.alpha = (self.v_magnitude / 100) * np.array([[math.cos(self.theta * (math.pi / 180))], [-math.sin(self.theta * (math.pi / 180))]])
        else:
            self.alpha = np.array([[0.0], [0.0]])

        self.v += self.a + self.alpha - (self.v / FRICTIONAL_COEFFICIENT)
        self.s += self.v

        # self.rect.center = (int(self.s[0]), int(self.s[1]))

        if self.s[0] > WIDTH or self.s[0] < 0 or self.s[1] > HEIGHT or self.s[1] < 0:
            self.v *= 0
            self.s = np.array([[WIDTH/4], [HEIGHT/2]])
        
        else:
            self.rect.center = (int(self.s[0]), int(self.s[1]))

    def rotate(self, theta):
        self.image = pygame.transform.rotate(self.original_image, self.theta)
        self.theta += theta
        self.theta %= 360
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # return rotated_image, new_rect

    def accelerate(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.const_a = (DRIVING_FORCE) / CAR_MASS

            self.a = self.const_a * np.array([[math.cos(self.theta * (math.pi / 180))], [-math.sin(self.theta * (math.pi / 180))]])

            # transform_matrix = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
            # self.a = np.matmul((transform_matrix * self.const_a), np.array([[0.0], [-1.0]]))
            # self.a = self.const_a * (np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]]) * np.array([[1.0], [1.0]]))
            # print(self.a)
        else:
            self.a *= 0
            

# player = Player('')

# print(player.s)