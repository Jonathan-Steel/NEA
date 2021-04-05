import pygame
import random
import xml.etree.ElementTree as ET
import math

from settings import *
from library import *
from sprites import *

# TILES = [pygame.image.load('assets/land_grass04.png'),
# pygame.image.load('assets/road_asphalt01.png'),
# pygame.image.load('assets/road_asphalt02.png'),
# pygame.image.load('assets/road_asphalt03.png'),
# pygame.transform.rotate(pygame.image.load('assets/road_asphalt03.png'), 90),
# pygame.transform.rotate(pygame.image.load('assets/road_asphalt03.png'), 180),
# pygame.transform.rotate(pygame.image.load('assets/road_asphalt03.png'), 270)]

class Tilemap:

    def __init__(self, tile_width, tile_height, width, height, game):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.width = width
        self.height = height
        self.game = game
        self.spritesheet = load_spritesheet('assets/original/Spritesheets/spritesheet_tiles.png', 'assets/original/Spritesheets/spritesheet_tiles.xml')
        self.tiles = [pygame.transform.scale(tile, (self.tile_width, self.tile_height)) for tile in self.spritesheet]
        # self.tilemap = [[0 for i in range(self.width)] for i in range(self.height)]
        self.tilemap = self.read_tilemap('map.txt')
        self.current_tile = 17
        self.current_tile_input = ""

    def preview(self):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.line(self.game.screen, (55, 55, 55), (x*self.tile_width, y*self.tile_height), (x*self.tile_width, (y+1)*self.tile_height))
                pygame.draw.line(self.game.screen, (55, 55, 55), (x*self.tile_width, y*self.tile_height), ((x+1)*self.tile_width, y*self.tile_height))
    
    def display_tiles(self):
        for x in range(self.width):
            for y in range(self.height):
                self.game.screen.blit(self.tiles[self.tilemap[y][x]], (x*self.tile_width, y*self.tile_height))

    def change_tile(self, x, y):
        self.tilemap[y][x] = self.current_tile

    def read_tilemap(self, filename):
        tilemap = []
        with open(filename, 'r') as myFile:
            for line in myFile:
                line = line.strip('\n')
                line = line.split('\t')
                line.remove('')
                tilemap.append([int(character) for character in line])
        return tilemap

    def write_tilemap(self, filename):
        with open(filename, 'w') as myFile:
            for line in self.tilemap:
                string = ''
                for tile in line:
                    string += str(tile) + '\t'
                string += '\n'
                myFile.write(string)

    def change_current_tile(self):
        if int(self.current_tile_input) < len(self.tiles):
            self.current_tile = int(self.current_tile_input)
            self.current_tile_input = ""
        else:
            print('Tile Number out of range!')
        self.current_tile_input = ""

class Game:

    # Initialises the game
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.clock = pygame.time.Clock()

        self.running = True

        pygame.display.set_caption(TITLE)

        self.tilemap = Tilemap(tile_width=32, tile_height=32, width=48, height=27, game=self)

    def main_menu(self):
        pass
    
    # Starts a new game (round)
    def new(self):
        # Initialises a general sprite group
        self.all_sprites = pygame.sprite.Group()
        # self.menu_sprites = pygame.sprite.Group()
        self.menu_buttons = []
        self.game_sprites = pygame.sprite.Group()

        # self.main_menu_header = get_text(text='NEA', size=128, y=300)
        self.map_editor_button = Button(game=self, x=(WIDTH // 2 - 100), y=HEIGHT // 2, text="Map Editor")
        self.menu_buttons.append(self.map_editor_button)

        self.start_game_button = Button(game=self, x=(WIDTH // 2 + 100), y=HEIGHT // 2, text="Start Game")
        self.menu_buttons.append(self.start_game_button)

        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.game_sprites.add(self.player)

        self.mouse_position = (0, 0)

        self.mode = "Main Menu"

        self.run()

    # Game loop
    def run(self):
        self.playing = True
        
        while self.playing:
            # Frame rate
            self.clock.tick(FPS)

            # Checks for any events (e.g. close button)
            self.events()

            # Updates sprites
            self.update()

            # Draws objects to screen
            self.draw()

    # Checks for events
    def events(self):
        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                self.mouse_position = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if self.mode == "Main Menu":
                    if self.map_editor_button.hover == True:
                        self.mode = "Map Editor"
                        # print("Hello")
                    elif self.start_game_button.hover == True:
                        self.mode = "Game"

                elif self.mode == "Map Editor":
                    self.tilemap.change_tile(event.pos[0] // self.tilemap.tile_width, event.pos[1] // self.tilemap.tile_height)

            if event.type == pygame.KEYDOWN:
                if self.mode == "Map Editor":
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_0] or keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4] or keys[pygame.K_5] or keys[pygame.K_6] or keys[pygame.K_7] or keys[pygame.K_8] or keys[pygame.K_9]:
                        self.tilemap.current_tile_input += chr(event.key)
                        print(self.tilemap.current_tile_input)
                    elif keys[pygame.K_RETURN]:
                        self.tilemap.change_current_tile()

            #     if event.unicode in [str(i) for i in range(7)]:
            #         self.tilemap.current_tile = int(event.unicode)

    # Updates sprites
    def update(self):
        if self.mode == "Main Menu":
            self.map_editor_button.update()
            # if self.map_editor_button.clicked:
            #     self.map_editor_button.clicked = False
            #     self.mode = "Map Editor"

            self.start_game_button.update()
            # if self.start_game_button.clicked:
            #     self.start_game_button.clicked = False
            #     self.mode = "Game"
            #     print(self.mode)

        elif self.mode == "Game":
            self.game_sprites.update()

        elif self.mode == "Map Editor":
            pass

    # Draws objects to screen
    def draw(self):
        self.screen.fill(WHITE)

        if self.mode == "Main Menu":
            self.blit_text(*get_text(text='NEA', size=128, y=300))

            self.map_editor_button.draw(self.screen)
            self.start_game_button.draw(self.screen)

            # self.menu_sprites.draw(self.screen)

        elif self.mode == "Game":
            self.tilemap.display_tiles()

            # self.tilemap.preview()

            self.all_sprites.draw(self.screen)

            pygame.draw.rect(self.screen, RED, self.player.rect, 3)

            self.blit_text(*get_text(f"a = ({self.player.a[0]}, {self.player.a[1]}), v = ({int(self.player.v[0])}, {int(self.player.v[1])}), s = ({int(self.player.s[0])}, {int(self.player.s[1])}), theta = {self.player.theta}", colour=BLACK, size=14))

        elif self.mode == "Map Editor":
            self.tilemap.display_tiles()
            self.tilemap.preview()

            # Tiles Palette

        # After drawing everything flip the display
        pygame.display.flip()

    def show_start_screen(self):

        self.screen.fill(WHITE)

        # self.tilemap.current_tile = 17
        # for x in range(self.tilemap.width):
        #     for y in range(self.tilemap.height):
        #         self.tilemap.change_tile(x, y)

        # print(self.tilemap.tilemap)
        
        # self.tilemap.display_tiles()

        self.blit_text(*get_text(text='NEA', size=128, y=300))
        self.blit_text(*get_text(text='Press any button to continue', y=500))

        # new_button = Button(game=self, x=WIDTH // 2, y=HEIGHT // 2, text="Map Editor")
        # new_button.draw(self.screen)

        pygame.display.flip()

        self.wait_for_key()

    def show_go_screen(self):
        pass

    def map_editor(self):
        pass

    def blit_text(self, TextSurf, TextRect):
        self.screen.blit(TextSurf, TextRect)

    def wait_for_key(self):
        key_not_pressed = True
        while key_not_pressed:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    key_not_pressed = False
                if event.type == pygame.KEYUP:
                    key_not_pressed = False

    def angle_between_player_and_mouse(self):

        ## Player to Mouse Pointer Angle ##

        delta_x = self.mouse_position[0] - int(self.player.s[0])
        delta_y = (self.mouse_position[1] - int(self.player.s[1])) * -1

        theta = None

        # Cursor higher than car
        if delta_x > 0 and delta_y > 0:
            theta = math.atan(delta_y/delta_x)
        if delta_x == 0 and delta_y > 0:
            theta = (math.pi / 2)
        if delta_x < 0 and delta_y > 0:
            theta = ((math.pi / 2) - (math.atan(delta_y/delta_x) * -1)) + (math.pi / 2)

        # Cursor at car's height
        if delta_x >= 0 and delta_y == 0:
            theta = 0
        if delta_x < 0 and delta_y == 0:
            theta = math.pi

        # Cursor at lower than car
        if delta_x > 0 and delta_y < 0:
            theta = 2 * math.pi + math.atan(delta_y/delta_x)
            # theta = math.atan(delta_y / delta_x)
        if delta_x == 0 and delta_y < 0:
            theta = 1.5 * math.pi
            # theta = -(0.5 * math.pi)
        if delta_x < 0 and delta_y < 0:
            theta = math.pi + math.atan(delta_y/delta_x)
            # theta = - (math.pi - math.atan(delta_y/delta_x))
        
        print(f'delta_x = {delta_x}, delta_y = {delta_y}, theta = {theta * 180/math.pi}')

        return theta

game = Game()

game.show_start_screen()

while game.running:

    game.main_menu()

    game.new()

    # game.show_go_screen()

game.tilemap.write_tilemap('map.txt')

pygame.quit()