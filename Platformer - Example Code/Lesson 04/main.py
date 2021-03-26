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
		self.platforms = pg.sprite.Group()
		self.player = Player(self)
		self.all_sprites.add(self.player)
		for plat in PLATFORM_LIST:
			p = Platform(*plat) # Explodes list into four components
			self.all_sprites.add(p)
			self.platforms.add(p)
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
		# Check if player hits a platform - only if falling
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.platforms, False)
			if hits:
				self.player.pos.y = hits[0].rect.top + 1
				self.player.vel.y = 0

	def events(self):
		# Game Loop - Events
		for event in pg.event.get():
			# Checks for closing the window
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.player.jump()

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