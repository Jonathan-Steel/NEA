import pygame
import random
import xml.etree.ElementTree as ET
import numpy as np
import math

from library import *
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, game, car_model, colour):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.car_model = car_model
        self.colour = colour

        self.spritesheet = load_spritesheet('assets/original/Spritesheets/spritesheet_vehicles.png', 'assets/original/Spritesheets/spritesheet_vehicles.xml')
        self.image_file = self.spritesheet[self.colour * 10 + self.car_model]
        self.original_image = pygame.transform.rotate(pygame.transform.scale(self.image_file, (self.image_file.get_width() // 2, self.image_file.get_height() // 2)), -90)
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.s = np.array([[335.], [785.]])
        self.v = np.array([[0.0], [0.0]])
        self.const_a = 0
        self.a = np.array([[0.0], [0.0]])

        self.rect.center = (int(self.s[0]), int(self.s[1]))

        self.theta = 0

        self.collides = False
        self.checkpoint = "start"

    def update(self):
        self.v_magnitude = np.linalg.norm(self.v)

        self.collision = self.collide()

        self.update_checkpoint()
        
        # print(self.collision)

        keys = pygame.key.get_pressed()

        delta_theta = 0
        if keys[pygame.K_a] and not(keys[pygame.K_d]):
            delta_theta = self.v_magnitude / 4
        if keys[pygame.K_d] and not(keys[pygame.K_a]):
            delta_theta = -(self.v_magnitude / 4)

        self.rotate(delta_theta)

        self.accelerate()

        if self.a[0] == 0 and self.a[1] == 0 and delta_theta != 0:
            self.alpha = (self.v_magnitude / 10) * np.array([[math.cos(self.theta * (math.pi / 180))], [-math.sin(self.theta * (math.pi / 180))]])
        else:
            self.alpha = np.array([[0.0], [0.0]])

        self.v += self.a + self.alpha - (self.v / FRICTIONAL_COEFFICIENT) + (2 * self.v_magnitude * self.collision)
        # self.v += self.a + self.alpha - (self.v / FRICTIONAL_COEFFICIENT) + (2 * collision)
        self.s += self.v

        # self.rect.center = (int(self.s[0]), int(self.s[1]))

        if self.s[0] > WIDTH or self.s[0] < 0 or self.s[1] > HEIGHT or self.s[1] < 0:
            self.v *= 0
            self.s = np.array([[335.], [785.]])
        
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

    def collide(self):
        collision_tolerance = 0
        for wall in self.game.walls:
            if self.rect.colliderect(self.game.walls[wall]):
                
                self.collides = True
                colliding_wall = self.game.walls[wall]
                # print(f"Collision detected with wall at {wall}!")

                # Left (of the wall)
                if self.theta == 0:
                    return np.array([[-1.0], [0.0]])
                # Left or Bottom
                elif self.theta > 0 and self.theta < 90:
                    if (wall[0] - 1, wall[1]) in self.game.walls: # Condition change to check whether has left surface
                        return np.array([[0.0], [1.0]])
                    else:
                        return np.array([[-1.0], [0.0]])
                # Bottom
                elif self.theta == 90:
                    return np.array([[0.0], [1.0]])
                # Right or Bottom
                elif self.theta > 90 and self.theta < 180:
                    if (wall[0] + 1, wall[1]) in self.game.walls:
                        return np.array([[0.0], [1.0]])
                    else:
                        return np.array([[1.0], [0.0]])
                # Right
                elif self.theta == 180:
                    return np.array([[1.0], [0.0]])
                # Right or Top
                elif self.theta > 180 and self.theta < 270:
                    if (wall[0] + 1, wall[1]) in self.game.walls:
                        return np.array([[0.0], [-1.0]])
                    else:
                        return np.array([[1.0], [0.0]])
                # Top
                elif self.theta == 270:
                    return np.array([[0.0], [-1.0]])
                # Left or top
                elif self.theta > 270 and self.theta < 360:
                    if (wall[0] - 1, wall[1]) in self.game.walls:
                        return np.array([[0.0], [-1.0]])
                    else:
                        return np.array([[-1.0], [0.0]])

                # # Left (of the wall)
                # if self.theta == 0:
                #     return np.array([[-1.0], [0.0]])
                # # Left or Bottom
                # elif self.theta > 0 and self.theta < 90:
                #     if self.rect.top >= (colliding_wall.rect.bottom + collision_tolerance): # Condition change to check 15 frames earlier
                #         return np.array([[0.0], [1.0]])
                #     else:
                #         return np.array([[-1.0], [0.0]])
                # # Bottom
                # elif self.theta == 90:
                #     return np.array([[0.0], [1.0]])
                # # Right or Bottom
                # elif self.theta > 90 and self.theta < 180:
                #     if self.rect.top >= (colliding_wall.rect.bottom + collision_tolerance):
                #         return np.array([[0.0], [1.0]])
                #     else:
                #         return np.array([[1.0], [0.0]])
                # # Right
                # elif self.theta == 180:
                #     return np.array([[1.0], [0.0]])
                # # Right or Top
                # elif self.theta > 180 and self.theta < 270:
                #     if self.rect.bottom <= (colliding_wall.rect.top - collision_tolerance):
                #         return np.array([[0.0], [1.0]])
                #     else:
                #         return np.array([[1.0], [0.0]])
                # # Top
                # elif self.theta == 270:
                #     return np.array([[0.0], [-1.0]])
                # # Left or top
                # elif self.theta > 270 and self.theta < 360:
                #     if self.rect.bottom <= (colliding_wall.rect.top - collision_tolerance):
                #         return np.array([[0.0], [1.0]])
                #     else:
                #         return np.array([[-1.0], [0.0]])

                # if self.theta <= 45 or self.theta > 315:
                #     return np.array([[-1.0], [0.0]])

                # elif self.theta <= 135 or self.theta > 45:
                #     return np.array([[0.0], [1.0]])
                
                # elif self.theta <= 225 or self.theta > 135:
                #     return np.array([[1.0], [0.0]])

                # elif self.theta <= 315 or self.theta > 225:
                #     return np.array([[0.0], [-1.0]])

                # # Wall Top - Car Bottom
                # if abs(colliding_wall.rect.top - self.rect.bottom) < collision_tolerance:
                #     print("Wall: Top\t\tCar: Bottom")
                #     return np.array([[0.0], [-1.0]]) * abs(self.v[1])

                # # Wall Bottom - Car Top
                # elif abs(colliding_wall.rect.bottom - self.rect.top) < collision_tolerance:
                #     print("Wall: Bottom\t\tCar: Top")
                #     return np.array([[0.0], [1.0]]) * abs(self.v[1])

                # # Wall Left - Car Right
                # elif abs(colliding_wall.rect.left - self.rect.right) < collision_tolerance:
                #     print("Wall: Left\t\tCar: Right")
                #     return np.array([[-1.0], [0.0]]) * abs(self.v[0])

                # # Wall Right - Car Left
                # elif abs(colliding_wall.rect.right - self.rect.left) < collision_tolerance:
                #     print("Wall: Right\t\tCar: Left")
                #     return np.array([[1.0], [0.0]]) * abs(self.v[0])     
            else:
                self.collides = False

        return np.array([[0.0], [0.0]])

    def update_checkpoint(self):
        if self.checkpoint == "midpoint":
            for start_line in self.game.start_line:
                if self.rect.colliderect(self.game.start_line[start_line]):
                    self.checkpoint = "start"
                    if len(self.game.lap_times) > 0:
                        if ((self.game.delta_ticks - sum(self.game.lap_times))/1000 % 60) > 5:
                            self.game.lap += 1
                            self.game.lap_times.append(self.game.delta_ticks - sum(self.game.lap_times))
                    else:
                        self.game.lap += 1
                        self.game.lap_times.append(self.game.delta_ticks)

        elif self.checkpoint == "start":
            for midpoint in self.game.midpoint_line:
                if self.rect.colliderect(self.game.midpoint_line[midpoint]):
                    self.checkpoint = "midpoint"

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # important to reference superclass
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x * 32, self.y * 32, 32, 32)
        self.color = RED
    def draw(self, surface):
        s = pygame.Surface((32, 32))
        s.set_alpha(128)
        s.fill(self.color)
        surface.blit(s, self.rect)

class StartLine(Wall):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = GREEN

class Midpoint(Wall):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = BLUE

class PlayerTemplate:
    def __init__(self):
        self.cars = LinkedList(0)
        self.cars.add(1)
        self.cars.add(2)
        self.cars.add(3)
        self.cars.add(4)

        self.colours = LinkedList(0)
        self.colours.add(1)
        self.colours.add(2)
        self.colours.add(3)
        self.colours.add(4)

        self.car_model = self.cars.head_node
        self.colour = self.colours.head_node

        self.spritesheet = load_spritesheet('assets/original/Spritesheets/spritesheet_vehicles.png', 'assets/original/Spritesheets/spritesheet_vehicles.xml')
        self.image_file = self.change_sprite()
        self.image = pygame.transform.rotate(self.image_file, -90)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
    
    def change_sprite(self):
        return self.spritesheet[self.colour.data * 10 + self.car_model.data]

    def next_sprite(self, change):
        if change == "Car":
            if self.car_model.next_node:
                self.car_model = self.car_model.next_node
            else:
                self.car_model = self.cars.head_node
        elif change == "Colour":
            if self.colour.next_node:
                self.colour = self.colour.next_node
            else:
                self.colour = self.colours.head_node
        self.change_sprite()

    def return_final_changes(self):
        return self.car_model.data, self.colour.data

    def update(self):
        self.image_file = self.change_sprite()
        self.image = pygame.transform.rotate(self.image_file, -90)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2 - 100)

    def draw(self, screen):
        screen.blit(self.image, self.rect)