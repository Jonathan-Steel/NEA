import pygame
import random
import xml.etree.ElementTree as ET
import math

from settings import *
from library import *
from sprites import *

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
        # MAIN MENU MODE
        self.menu_buttons = []
        self.map_editor_button = Button(game=self, x=(WIDTH // 2 - 100), y=HEIGHT // 2, text="Map Editor")
        self.menu_buttons.append(self.map_editor_button)

        self.start_game_button = Button(game=self, x=(WIDTH // 2 + 100), y=HEIGHT // 2, text="Start Game")
        self.menu_buttons.append(self.start_game_button)

        self.login_button = Button(game=self, x=(WIDTH // 2 - 100), y=(HEIGHT // 2 + 100), text="Login")
        self.menu_buttons.append(self.login_button)

        self.register_button = Button(game=self, x=(WIDTH // 2 + 100), y=(HEIGHT // 2 + 100), text="Register")
        self.menu_buttons.append(self.register_button)

    def setup_login(self):
        self.login_boxes = []

        self.username_input = InputBox(game=self, x=(WIDTH // 2), y=(HEIGHT // 2 - 48), placeholder="Username")
        self.login_boxes.append(self.username_input)

        self.password_input = PasswordBox(game=self, x=(WIDTH // 2), y=(HEIGHT // 2), placeholder="Password")
        self.login_boxes.append(self.password_input)

        self.submit_button = Button(game=self, x=(WIDTH // 2), y=(HEIGHT // 2 + 48), text="Submit")
        self.login_boxes.append(self.submit_button)

    def setup_register(self):
        self.register_boxes = []

        self.username_input.content = ""
        self.register_boxes.append(self.username_input)

        self.password_input.content = ""
        self.register_boxes.append(self.password_input)

        self.register_boxes.append(self.submit_button)

    def start_round(self):
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.game_sprites.add(self.player)

        self.lap = 1
        self.lap_times = []

        self.start_ticks = pygame.time.get_ticks()
        self.delta_ticks = 0
        self.menu_ticks = 0

    # Starts a new game (round)
    def new(self):
        # Initialises a general sprite group
        self.all_sprites = pygame.sprite.Group()
        # self.menu_sprites = pygame.sprite.Group()
        self.game_sprites = pygame.sprite.Group()

        # WALLS and other SPECIAL TILES
        self.walls = self.read_tile("wall")
        self.start_line = self.read_tile("start line")
        self.midpoint_line = self.read_tile("midpoint line")

        self.end_race_button = Button(self, x=(WIDTH // 2), y=(HEIGHT // 2 + 72), text="Return to menu")

        self.main_menu()

        self.setup_login()

        self.setup_register()

        # GAME MODE
        # self.player = Player(self)
        # self.all_sprites.add(self.player)
        # self.game_sprites.add(self.player)

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
                current_coords = (event.pos[0] // self.tilemap.tile_width, event.pos[1] // self.tilemap.tile_height)

                if self.mode == "Main Menu":
                    if self.map_editor_button.hover == True:
                        self.mode = "Map Editor"
                    elif self.start_game_button.hover == True:
                        self.start_ticks = pygame.time.get_ticks()
                        self.mode = "Countdown"
                        # self.start_round()
                        # self.mode = "Game"
                    elif self.login_button.hover == True:
                        self.mode = "Login"
                        self.username_input.content = ""
                        self.password_input.content = ""
                    elif self.register_button.hover == True:
                        self.mode = "Register"
                        self.username_input.content = ""
                        self.password_input.content = ""

                elif self.mode == "Pause":
                    if self.end_race_button.hover == True:
                        self.game_sprites.remove(self.player)
                        self.all_sprites.remove(self.player)
                        self.mode = "Main Menu"

                elif self.mode == "Login":
                    for box in self.login_boxes:
                        if box.hover:
                            box.selected = True
                            for selected_box in self.login_boxes:
                                if selected_box == box:
                                    continue
                                selected_box.selected = False

                elif self.mode == "Register":
                    for box in self.register_boxes:
                        if box.hover:
                            box.selected = True
                            for selected_box in self.register_boxes:
                                if selected_box == box:
                                    continue
                                selected_box.selected = False

                elif self.mode == "Map Editor":
                    self.tilemap.change_tile(event.pos[0] // self.tilemap.tile_width, event.pos[1] // self.tilemap.tile_height)

                elif self.mode == "Walls Editor":
                    if not(current_coords in self.walls):
                        self.walls[current_coords] = (Wall(current_coords[0], current_coords[1]))

                elif self.mode == "Walls Editor (Eraser Mode)":
                    if current_coords in self.walls:
                        self.walls.pop(current_coords)

                elif self.mode == "Start Line Editor":
                    if not(current_coords in self.start_line):
                        self.start_line[current_coords] = (StartLine(current_coords[0], current_coords[1]))

                elif self.mode == "Start Line Editor (Eraser Mode)":
                    if current_coords in self.start_line:
                        self.start_line.pop(current_coords)
                
                elif self.mode == "Midpoint Editor":
                    if not(current_coords in self.midpoint_line):
                        self.midpoint_line[current_coords] = (Midpoint(current_coords[0], current_coords[1]))

                elif self.mode == "Midpoint Editor (Eraser Mode)":
                    if current_coords in self.midpoint_line:
                        self.midpoint_line.pop(current_coords)

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if self.mode == "Map Editor":

                    if keys[pygame.K_0] or keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4] or keys[pygame.K_5] or keys[pygame.K_6] or keys[pygame.K_7] or keys[pygame.K_8] or keys[pygame.K_9]:
                        self.tilemap.current_tile_input += chr(event.key)
                        print(self.tilemap.current_tile_input)
                    elif keys[pygame.K_RETURN]:
                        self.tilemap.change_current_tile()

                    elif self.tilemap.current_tile_input == "" and keys[pygame.K_w]:
                        self.mode = "Walls Editor"

                    elif self.tilemap.current_tile_input == "" and keys[pygame.K_s]:
                        self.mode = "Start Line Editor"

                    elif self.tilemap.current_tile_input == "" and keys[pygame.K_m]:
                        self.mode = "Midpoint Editor"

                    elif keys[pygame.K_ESCAPE]:
                        self.mode = "Main Menu"

                elif self.mode == "Game":
                    if keys[pygame.K_ESCAPE]:
                        self.mode = "Pause"

                elif self.mode == "Pause":
                    if keys[pygame.K_ESCAPE]:
                        self.mode = "Game"
                    
                elif self.mode == "Login":
                    if keys[pygame.K_ESCAPE]:
                        self.mode = "Main Menu"
                    for box in self.login_boxes:
                        if box.selected:
                            if keys[pygame.K_ESCAPE]:
                                box.selected = False
                            elif keys[pygame.K_BACKSPACE] and len(box.content) > 0:
                                box.content = box.content[:-1]
                            else:
                                box.content += event.unicode

                elif self.mode == "Register":
                    if keys[pygame.K_ESCAPE]:
                        self.mode = "Main Menu"
                    for box in self.register_boxes:
                        if box.selected:
                            if keys[pygame.K_ESCAPE]:
                                box.selected = False
                            elif keys[pygame.K_BACKSPACE] and len(box.content) > 0:
                                box.content = box.content[:-1]
                            else:
                                box.content += event.unicode
                
                elif self.mode == "Walls Editor" or self.mode == "Walls Editor (Eraser Mode)":
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        self.write_tile("wall")
                        self.mode = "Map Editor"
                    elif keys[pygame.K_e]:
                        if self.mode == "Walls Editor":
                            self.mode = "Walls Editor (Eraser Mode)"
                        else:
                            self.mode = "Walls Editor"
                
                elif self.mode == "Start Line Editor" or self.mode == "Start Line Editor (Eraser Mode)":
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        self.write_tile("start line")
                        self.mode = "Map Editor"
                    elif keys[pygame.K_e]:
                        if self.mode == "Start Line Editor":
                            self.mode = "Start Line Editor (Eraser Mode)"
                        else:
                            self.mode = "Start Line Editor"
                
                elif self.mode == "Midpoint Editor" or self.mode == "Midpoint Editor (Eraser Mode)":
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        self.write_tile("midpoint line")
                        self.mode = "Map Editor"
                    elif keys[pygame.K_e]:
                        if self.mode == "Midpoint Editor":
                            self.mode = "Midpoint Editor (Eraser Mode)"
                        else:
                            self.mode = "Midpoint Editor"

            #     if event.unicode in [str(i) for i in range(7)]:
            #         self.tilemap.current_tile = int(event.unicode)

    # Updates sprites
    def update(self):
        pygame.display.set_caption(TITLE + " - " + self.mode)
        if self.mode == "Main Menu":
            for button in self.menu_buttons:
                button.update()

        elif self.mode == "Game":
            self.game_sprites.update()
            self.delta_ticks = pygame.time.get_ticks() - self.start_ticks - self.menu_ticks

        elif self.mode == "Pause":
            self.menu_ticks = pygame.time.get_ticks() - self.delta_ticks
            self.end_race_button.update()

        elif self.mode == "Map Editor":
            pass

        elif self.mode == "Login":
            for box in self.login_boxes:
                box.update()

        elif self.mode == "Register":
            for box in self.register_boxes:
                box.update()

        elif self.mode == "Countdown":
            self.delta_ticks = pygame.time.get_ticks() - self.start_ticks
            if int(self.delta_ticks/1000 % 60) > 3:
                self.start_round()
                self.mode = "Game"

    # Draws objects to screen
    def draw(self):
        self.screen.fill(WHITE)

        if self.mode == "Main Menu":
            self.blit_text(*get_text(text='NEA', size=128, y=300))

            for button in self.menu_buttons:
                button.draw(self.screen)

        elif self.mode == "Game":
            self.tilemap.display_tiles()

            self.tilemap.preview()

            for key in self.walls:
                self.walls[key].draw(self.screen)
            for key in self.start_line:
                self.start_line[key].draw(self.screen)
            for key in self.midpoint_line:
                self.midpoint_line[key].draw(self.screen)

            self.all_sprites.draw(self.screen)

            pygame.draw.rect(self.screen, RED, self.player.rect, 3)

            # self.blit_text(*get_text(f"a = ({self.player.a[0]}, {self.player.a[1]}), v = ({int(self.player.v[0])}, {int(self.player.v[1])}), s = ({int(self.player.s[0])}, {int(self.player.s[1])}), theta = {self.player.theta}, mouse position = {self.mouse_position}", colour=BLACK, size=18))
            # self.blit_text(*get_text(f"v = {self.player.a} + {self.player.alpha} - {self.player.v / FRICTIONAL_COEFFICIENT} + {0.5 * self.player.v_magnitude * self.player.collision}", y=HEIGHT // 2 + 100, size=24))
            # self.blit_text(*get_text(f"v = {np.round(self.player.a, decimals=1)} + {np.round(self.player.alpha, decimals=1)} - FRICTION + {np.round(0.5 * self.player.v_magnitude * self.player.collision, decimals=1)}", y=HEIGHT // 2 + 100, size=24))
            self.blit_text(*get_text(f"Lap = {self.lap}, Checkpoint = {self.player.checkpoint}", y=HEIGHT // 2 + 100, size=24))
            self.blit_text(*get_text(self.display_lap_times(), y=HEIGHT // 2 + 25, size=24))
            self.blit_text(*get_text(clean_time(self.delta_ticks), size=18))

            if self.player.collides:
                self.blit_text(*get_text("Collides", colour=RED, size=100, y=(HEIGHT // 2 - 100)))

        elif self.mode in EDITOR_MODES:
            self.tilemap.display_tiles()
            self.tilemap.preview()

            for key in self.walls:
                self.walls[key].draw(self.screen)

            for key in self.start_line:
                self.start_line[key].draw(self.screen)

            for key in self.midpoint_line:
                self.midpoint_line[key].draw(self.screen)

        elif self.mode == "Pause":
            self.blit_text(*get_text("Pause", size=72, y=(HEIGHT / 2 - 54)))
            self.blit_text(*get_text("Press Esc to resume.", size=18))
            self.end_race_button.draw(self.screen)

        elif self.mode == "Countdown":
            self.blit_text(*get_text(f"{(3 - int(self.delta_ticks/1000 % 60)):1d}", size=144))

        elif self.mode == "Login":
            for box in self.login_boxes:
                box.draw(self.screen)

        elif self.mode == "Register":
            for box in self.register_boxes:
                box.draw(self.screen)

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

    def write_tile(self, tile_type):
        if tile_type == "wall":
            with open('walls.txt', 'w') as myFile:
                for wall in self.walls:
                    myFile.write(str(wall) + "\n")
        elif tile_type == "start line":
            with open('start_line.txt', 'w') as myFile:
                for start_line in self.start_line:
                    myFile.write(str(start_line) + "\n")
        elif tile_type == "midpoint line":
            with open('midpoint_line.txt', 'w') as myFile:
                for midpoint_line in self.midpoint_line:
                    myFile.write(str(midpoint_line) + "\n")
        else:
            print("Tile Type Invalid!")

    def read_tile(self, tile_type):
        if tile_type == "wall":
            with open('walls.txt', 'r') as myFile:
                walls = {}
                for line in myFile:
                    line = line.strip('\n')
                    line = line.split(',')
                    x = int(line[0].strip("("))
                    y = int(line[1].strip(")"))
                    walls[(x, y)] = Wall(x, y)
                return walls
        elif tile_type == "start line":
            with open('start_line.txt', 'r') as myFile:
                start_line = {}
                for line in myFile:
                    line = line.strip('\n')
                    line = line.split(',')
                    x = int(line[0].strip("("))
                    y = int(line[1].strip(")"))
                    start_line[(x, y)] = StartLine(x, y)
                return start_line
        elif tile_type == "midpoint line":
            with open('midpoint_line.txt', 'r') as myFile:
                midpoint_line = {}
                for line in myFile:
                    line = line.strip('\n')
                    line = line.split(',')
                    x = int(line[0].strip("("))
                    y = int(line[1].strip(")"))
                    midpoint_line[(x, y)] = Midpoint(x, y)
                return midpoint_line
        else:
            print("Tile Type Invalid!")

    def display_lap_times(self):
        if len(self.lap_times) == 0:
            return ""
        output = f"{clean_time(self.lap_times[0])}"
        for time in self.lap_times:
            if self.lap_times.index(time) == 0:
                continue
            output += ", " + clean_time(time)
        return output

game = Game()

game.show_start_screen()

while game.running:

    game.new()

    # game.show_go_screen()

game.tilemap.write_tilemap('map.txt')

pygame.quit()