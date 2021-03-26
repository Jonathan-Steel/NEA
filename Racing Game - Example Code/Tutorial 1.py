import pygame

# Extremely necessary!
pygame.init()

# Defining the size of the window.
gameDisplay = pygame.display.set_mode((800,600))

# Setting the window header.
pygame.display.set_caption('Racing Game')

# In-game clock definition.
clock = pygame.time.Clock()

# Allows us to determine when to end the game.
crashed = False

# Begining the game loop.
while not crashed:

    # Creates a list of events for every fps.
    for event in pygame.event.get():

        # If someone hits the close button:
        if event.type == pygame.QUIT:

            crashed = True

        # Prints whatever event that pygame is tracking into the console.
        print(event)

    # Updates the display 
    pygame.display.update()

    # Frames per second
    clock.tick(60)

pygame.quit()
quit()

        

            

        
