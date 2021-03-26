# Pygame template
import pygame
import random

# Game Options
TITLE = "Platformer"
WIDTH = 360
HEIGHT = 480
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Game Loop
running = True
while running:
	# Loop runing at the right speed
	clock.tick(FPS)
	# Process input (events)
	for event in pygame.event.get():
		# Checks for closing the window
		if event.type == pygame.QUIT:
			running = False
	# Update

	# Draw / Render
	screen.fill(BLACK)
	# After drawing everything, flip the display
	pygame.display.flip()

pygame.quit()