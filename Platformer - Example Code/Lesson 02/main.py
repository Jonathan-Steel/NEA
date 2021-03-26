import pygame as pg
import random
from settings import *
from sprites import *

class Game:
	def __init__(self):
		# Initialize Game Window, etc
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.running = True

	def new(self):
		# Start a new game
		self.all_sprites = pg.sprite.Group()
		self.player = Player()
		self.all_sprites.add(self.player)
		self.run()

	def run(self):
		# Game Loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def update(self):
		# Game Loop - Update
		self.all_sprites.update()

	def events(self):
		# Game Loop - Events
		for event in pg.event.get():
			# Checks for closing the window
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False

	def draw(self):
		# Game Loop - Draw
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		# After drawing everything, flip the display
		pg.display.flip()

	def show_start_screen(self):
		# Game Start Screen
		pass

	def show_go_screen(self):
		pass

g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_go_screen()

pg.quit()