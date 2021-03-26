import pygame
import time
import random

# Extremely necessary!
pygame.init()

# Colour Definition
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

block_color = (53, 115, 255)
background_color = (247, 244, 145)

# Defining the size of the window.
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

# Setting the window header.
pygame.display.set_caption('Racing Game')

# In-game clock definition.
clock = pygame.time.Clock()

# Importing sprites:
carImg = pygame.image.load('racecar.png')

# Defining Image Width
car_width = 73 # Width in pixels

def win():

    message_display('You Won!', green)

# Used to count how many rectangles are dodged.
def things_dodged(count):

    font = pygame.font.SysFont(None, 25)

    text = font.render("Dodged: " + str(count), True, black)

    gameDisplay.blit(text, (0, 0))

# Displays objects on screen.
def things(thingx, thingy, thingw, thingh, color):

    # Draws a box to the screen.
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# Function which displays the car on the window.
def car(x, y):

    # Draws onto the window.
    gameDisplay.blit(carImg, (x, y))

def text_objects(text, font, color):

    textSurface = font.render(text, True, color)

    return textSurface, textSurface.get_rect()

# Displays text on the screen.
def message_display(text, color):

    # Defines font and font size.
    largeText = pygame.font.Font('freesansbold.ttf', 115)

    # Text surface and rectangle.
    TextSurf, TextRect = text_objects(text, largeText, color)

    # Centres the text rectangle.
    TextRect.center = ((display_width / 2), (display_height / 2))

    # Displays the text onto the screen.
    gameDisplay.blit(TextSurf, TextRect)

    # Updates the display.
    pygame.display.update()

    time.sleep(2)

    game_loop()

# Used when user crashes.
def crash():

    message_display('You Crashed!', black)

def game_loop():

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600

    thing_speed = 4

    thing_width = 100
    thing_height = 100

    dodged = 0

    # Allows us to determine when to end the game.
    gameExit = False

    # Begining the game loop.
    while not gameExit:

        # Creates a list of events for every fps.
        for event in pygame.event.get():

            # If someone hits the close button:
            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

            # If someone hits any key:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    x_change = -7

                elif event.key == pygame.K_RIGHT:

                    x_change = 7

            # If someone releases any key:
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

                    x_change = 0

        # Changes x value to allow movement.
        x += x_change

        # Sets a background colour.
        gameDisplay.fill(white)

        # Draws boxes
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)

        thing_starty += thing_speed

        # Displays the car.
        car(x, y)

        # Prints the score. Make sure score is always drawn last.
        things_dodged(dodged)

        # Logic for colliding with the edge of the screen.
        if x > display_width - car_width or x < 0:

            crash()

        # Detects if thing is off the screen.
        if thing_starty > display_height:

            # Sets y position to the top.
            thing_starty = 0 - thing_height

            # Sets random x position.
            thing_startx = random.randrange(0, display_width)

            # Increments score
            dodged += 1

            if dodged == 20:

                win()

            # Increases speed
            thing_speed += 0.7

            # Increases width
            thing_width += (dodged * 1.15)

        if y < thing_starty + thing_height:

            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                
                crash()

        # Updates the display. 
        pygame.display.update()

        # Frames per second.
        clock.tick(60)

# Runs the game loop
game_loop()

pygame.quit()
quit()

        

            

        
