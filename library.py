import pygame
import random
import xml.etree.ElementTree as ET
from settings import *

def load_spritesheet(pngfile, xmlfile):
    """Loads the spritesheet image, and splits it up into individual pygame surfaces based on data parsed from the xml file."""
    original_spritesheet = pygame.image.load(pngfile)
    
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    textures = []
    for texture in root.iter():
        subtexture = texture.attrib
        if len(subtexture) <= 1:
            continue
        textures.append(pygame.Surface.subsurface(original_spritesheet, (int(subtexture['x']), int(subtexture['y']), int(subtexture['width']), int(subtexture['height']))))
    
    return textures

def get_text(text, colour=BLACK, size=36, x=(WIDTH/2), y=(HEIGHT/2), font='fonts/Lato-Regular.ttf'):
    """Returns text objects for a given text."""
    font = pygame.font.Font(font, size)

    TextSurf = font.render(text, True, colour)

    TextRect = TextSurf.get_rect()

    TextRect.center = (x, y)

    return TextSurf, TextRect

def clean_time(ticks):
    """Converts a time in ticks to a format of {minutes}:{seconds}:{milliseconds}"""
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
        """Draws the button to the screen."""
        pygame.draw.rect(screen, self.bgColor, self.textRect, 0)
        screen.blit(self.textSurf, self.textRect)

    def update(self):
        """Updates the button's colour if the mouse is hovering over it."""
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

        # Text to be in the box if no text has been entered e.g. "Enter text here"
        self.placeholder = placeholder
        self.game = game
        self.hover = False
        self.content = ""
        self.selected = False

        self.textSurf, self.textRect = get_text(self.placeholder, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)

    def draw(self, screen):
        """Draws the box onto the screen."""
        if self.content == "":
            self.textSurf, self.textRect = get_text(self.placeholder, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)
        else:
            self.textSurf, self.textRect = get_text(self.content, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)
        pygame.draw.rect(screen, self.bgColor, self.textRect, 0)
        screen.blit(self.textSurf, self.textRect)

    def update(self):
        """Updates the input box to change its colour depending if the player is hovering over it."""
        self.check_hover()

        # Selected
        if not self.hover:
            if self.selected:
                self.bgColor = DARK_GREY
            else:
                self.bgColor = BLACK

    def check_hover(self):
        """Checks whether the mouse is hovering over the box."""
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
        """Replaces the content of the input box with a censor."""
        if self.content == "":
            self.textSurf, self.textRect = get_text(self.placeholder, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)
        else:
            censor = "•" * len(self.content)
            self.textSurf, self.textRect = get_text(censor, colour=self.textColor, size=self.fontsize, x=self.x, y=self.y)
        pygame.draw.rect(screen, self.bgColor, self.textRect, 0)
        screen.blit(self.textSurf, self.textRect)

class Node:
    """An element within a linked list that store data and connect to each other."""
    def __init__(self, data, next_node=None):
        self.data = data
        self.next_node = next_node
    # def __str__(self):
    #     return f"{self.data} -> {self.next_node.data}"

class LinkedList:
    def __init__(self, value):
        self.head_node = Node(value)

    def __str__(self):
        """Traverses the linked list and returns a string showing the traversal."""
        string = ""
        current_node = self.head_node
        while current_node:
            if current_node.data != None:
                string += str(current_node.data) + " -> "
            current_node = current_node.next_node
        return string

    def add(self, value):
        """Adds a new node at the beginning of the list."""
        new_node = Node(value, self.head_node)
        self.head_node = new_node

    def remove(self, value_to_remove):
        """Removes a node from the list and reconnects the chain of nodes around the one that has been removed."""
        current_node = self.head_node
        if current_node.data == value_to_remove:
            self.head_node = current_node.next_node
        else:
            while current_node:
                next_node = current_node.next_node
                if next_node.data == value_to_remove:
                    current_node.next_node = next_node.next_node
                    current_node = None
                else:
                    current_node = next_node