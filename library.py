import pygame
import random
import xml.etree.ElementTree as ET
from settings import *

def load_spritesheet(pngfile, xmlfile):
    original_spritesheet = pygame.image.load(pngfile)
    
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # textures = [subtexture.attrib for subtexture in root.iter()]
    # del textures[0]
    # print(textures[0])

    # dirt = pygame.Surface.subsurface(original_spritesheet, (int(textures[1]['x']), int(textures[1]['y']), int(textures[1]['width']), int(textures[1]['height'])))
    textures = []
    # counter = 0
    for texture in root.iter():
        subtexture = texture.attrib
        if len(subtexture) <= 1:
            continue
        # print(subtexture)
        # print(f"{counter} {subtexture['name']}")
        # counter += 1
        textures.append(pygame.Surface.subsurface(original_spritesheet, (int(subtexture['x']), int(subtexture['y']), int(subtexture['width']), int(subtexture['height']))))
    
    return textures

def get_text(text, colour=BLACK, size=36, x=(WIDTH/2), y=(HEIGHT/2), font='fonts/Lato-Regular.ttf'):

    font = pygame.font.Font(font, size)

    TextSurf = font.render(text, True, colour)

    TextRect = TextSurf.get_rect()

    TextRect.center = (x, y)

    return TextSurf, TextRect

def clean_time(ticks):
    return f"{int(ticks/60000 % 60):02d}:{int(ticks/1000 % 60):02d}:{ticks % 1000:02d}"

class Button:
    def __init__(self, game, x, y, fontsize=24, text="New Button", bgColor=BLACK, textColor=WHITE):
        self.x = x
        self.y = y
        self.fontsize = fontsize
        self.rawtext = text
        self.originalColor = bgColor
        self.bgColor = self.originalColor
        self.textColor = textColor
        self.game = game
        # self.clicked = False
        self.hover = False

        self.textSurf, self.textRect = get_text(self.rawtext, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgColor, self.textRect, 0)
        screen.blit(self.textSurf, self.textRect)

    def update(self):
        mouse_x, mouse_y = self.game.mouse_position
        if mouse_x >= self.textRect.left and mouse_x <= self.textRect.right and mouse_y >= self.textRect.top and mouse_y <= self.textRect.bottom:
            self.bgColor = GREY
            self.hover = True
        else:
            self.bgColor = self.originalColor
            self.hover = False

class InputBox:
    def __init__(self, game, x, y, fontsize=24, bgColor=BLACK, textColor=WHITE, placeholder="Enter text here"):
        self.x = x
        self.y = y
        self.fontsize = fontsize
        self.originalColor = bgColor
        self.bgColor = self.originalColor
        self.textColor = textColor
        self.placeholder = placeholder
        self.game = game
        self.hover = False
        self.content = ""
        self.selected = False

        self.textSurf, self.textRect = get_text(self.placeholder, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)

    def draw(self, screen):
        if self.content == "":
            self.textSurf, self.textRect = get_text(self.placeholder, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)
        else:
            self.textSurf, self.textRect = get_text(self.content, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)
        pygame.draw.rect(screen, self.bgColor, self.textRect, 0)
        screen.blit(self.textSurf, self.textRect)

    def update(self):
        self.check_hover()

        # Selected
        if not self.hover:
            if self.selected:
                self.bgColor = DARK_GREY
            else:
                self.bgColor = BLACK

    def check_hover(self):
        # Hover
        mouse_x, mouse_y = self.game.mouse_position
        if mouse_x >= self.textRect.left and mouse_x <= self.textRect.right and mouse_y >= self.textRect.top and mouse_y <= self.textRect.bottom:
            self.bgColor = GREY
            self.hover = True
        else:
            self.hover = False

class PasswordBox(InputBox):
    def __init__(self, game, x, y, fontsize=24, bgColor=BLACK, textColor=WHITE, placeholder="Enter text here"):
        super().__init__(game, x, y, fontsize, bgColor, textColor, placeholder)
    def draw(self, screen):
        if self.content == "":
            self.textSurf, self.textRect = get_text(self.placeholder, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)
        else:
            censor = "•" * len(self.content)
            self.textSurf, self.textRect = get_text(censor, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)
        pygame.draw.rect(screen, self.bgColor, self.textRect, 0)
        screen.blit(self.textSurf, self.textRect)

class HashTable:
    def __init__(self, array_size):
        self.array_size = array_size

    def hash_key(self, key):
        pass

    def assign(self, key, value):
        if type(key) == "tuple":
            pass
        else:
            print("Invalid key data type")

    def retrieve(self, key):
        pass