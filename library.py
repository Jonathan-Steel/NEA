import pygame
import random
import xml.etree.ElementTree as ET

def load_spritesheet(pngfile, xmlfile):
    original_spritesheet = pygame.image.load(pngfile)
    
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # textures = [subtexture.attrib for subtexture in root.iter()]
    # del textures[0]
    # print(textures[0])

    # dirt = pygame.Surface.subsurface(original_spritesheet, (int(textures[1]['x']), int(textures[1]['y']), int(textures[1]['width']), int(textures[1]['height'])))
    textures = []
    for texture in root.iter():
        subtexture = texture.attrib
        if len(subtexture) <= 1:
            continue
        # print(subtexture)
        textures.append(pygame.Surface.subsurface(original_spritesheet, (int(subtexture['x']), int(subtexture['y']), int(subtexture['width']), int(subtexture['height']))))
    
    return textures