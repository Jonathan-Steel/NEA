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

# Defining Image Width
car_width = 73 # Width in pixels

# Function which displays the car on the window.
def car(x, y):

    # Draws onto the window.
    gameDisplay.blit(carImg, (x, y))

def game_loop():

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    # Allows us to determine when to end the game.
    gameExit = False

    # Begining the game loop.
    while not gameExit:

        # Creates a list of events for every fps.
        for event in pygame.event.get():

            # If someone hits the close button:
            if event.type == pygame.QUIT:

                gameExit = True

            # If someone hits any key:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    x_change = -5

                elif event.key == pygame.K_RIGHT:

                    x_change = 5

            # If someone releases any key:
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

                    x_change = 0

        # Changes x value to allow movement.
        x += x_change

        # Sets a background colour.
        gameDisplay.fill(white)

        # Displays the car.
        car(x, y)

        # Logic for colliding with the edge of the screen.
        if x > display_width - car_width or x < 0:

            gameExit = True

        # Updates the display. 
        pygame.display.update()

        # Frames per second.
        clock.tick(60)

# Runs the game loop
game_loop()

pygame.quit()
quit()

        

            

        
