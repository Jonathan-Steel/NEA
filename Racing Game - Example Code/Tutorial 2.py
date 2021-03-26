import pygame

# Extremely necessary!
pygame.init()

# Colour Definition
black = (0, 0, 0)
white = (255, 255, 255)

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

# Function which displays the car on the window.
def car(x, y):

    # Draws onto the window.
    gameDisplay.blit(carImg, (x, y))

x = (display_width * 0.45)
y = (display_height * 0.8)

# Allows us to determine when to end the game.
crashed = False

# Begining the game loop.
while not crashed:

    # Creates a list of events for every fps.
    for event in pygame.event.get():

        # If someone hits the close button:
        if event.type == pygame.QUIT:

            crashed = True

    # Sets a background colour.
    gameDisplay.fill(white)

    # Displays the car.
    car(x, y)

    # Updates the display. 
    pygame.display.update()

    # Frames per second.
    clock.tick(60)

pygame.quit()
quit()

        

            

        
