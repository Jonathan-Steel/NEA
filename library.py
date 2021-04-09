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
            self.bgColor = RED
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

        self.textSurf, self.textRect = get_text(self.placeholder, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgColor, self.textRect, 0)
        screen.blit(self.textSurf, self.textRect)

    def update(self):
        # Hover
        mouse_x, mouse_y = self.game.mouse_position
        if mouse_x >= self.textRect.left and mouse_x <= self.textRect.right and mouse_y >= self.textRect.top and mouse_y <= self.textRect.bottom:
            self.bgColor = RED
            self.hover = True
        else:
            self.bgColor = self.originalColor
            self.hover = False