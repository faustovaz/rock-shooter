import pygame
import sys
from pygame.locals import *
import aircraft
import random
import enemy

class Game:

	screenSize 	= (800, 600)
	screen 		= pygame.display.set_mode(screenSize)
	clock 		= pygame.time.Clock()
	timeTick 	= 100

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Rock shooter - v-1.0")
		self.firstBackgroundImage = pygame.image.load("images/background.png").convert()
		self.secondBackgroundImage = pygame.image.load("images/background.png").convert()
		self.firstBackgroundPosition = (0,0) 
		self.secondBackgroundPosition = (0, (-1) * self.secondBackgroundImage.get_height())
		self.plane = aircraft.AirCraft()
		self.enemies = []
		self.enemyGenerateTime = 100

	def _scrollBackground(self):
		firstImageX, firstImageY = self.firstBackgroundPosition
		secondImageX, secondImageY = self.secondBackgroundPosition
		firstImageY = firstImageY + 2
		if (firstImageY > Game.screenSize[1]):
			firstImageY = self.firstBackgroundImage.get_height() * (-1)
		secondImageY = secondImageY + 2
		if (secondImageY > Game.screenSize[1]):
			secondImageY = self.firstBackgroundImage.get_height() * (-1)
		self.firstBackgroundPosition = (0, firstImageY)
		self.secondBackgroundPosition = (0, secondImageY)
		Game.screen.blit(self.firstBackgroundImage, self.firstBackgroundPosition)
		Game.screen.blit(self.secondBackgroundImage, self.secondBackgroundPosition)

	def run(self):
		while not self.plane.exploded:
			self._handleEvents()
			self._scrollBackground()
			self.checkHitEnemies()
			self.checkHitPlayer()
			self.updateEnemies()
			self.plane.updateBullets()
			self.plane.draw()
			self._generateEnemies()
			pygame.display.flip()
			Game.clock.tick(Game.timeTick)

	def _handleEvents(self):
			pressed=pygame.key.get_pressed()
			if pressed[K_LEFT]:
				self.plane.moveLeft()
			elif pressed[K_RIGHT]:
				self.plane.moveRight()
			elif pressed[K_UP]:
				self.plane.moveUp()
			elif pressed[K_DOWN]:
				self.plane.moveDown()
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_SPACE:
						self.plane.shoot()

	def updateEnemies(self):
		visibleEnemies = []
		for enemy in self.enemies:	
			if enemy.visible and not enemy.exploded:
				enemy.move()
				enemy.draw()
				visibleEnemies.append(enemy)
		self.enemies = visibleEnemies
	
	def _generateEnemies(self):
		if self.enemyGenerateTime == 0:
			self.enemyGenerateTime = 25
			self.enemies.append(enemy.Enemy())
		else:
			self.enemyGenerateTime = self.enemyGenerateTime - 1;

	def checkHitEnemies(self):
		for bullet in self.plane.bullets:
			for enemy in self.enemies:
				if bullet.rect.colliderect(enemy.rect) and not enemy.toExplode:
					bullet.visible = False
					enemy.explode()

	def checkHitPlayer(self):
		for enemy in self.enemies:
			if enemy.visible and self.plane.airCraftRect.colliderect(enemy.rect) and not self.plane.toExplode:
				enemy.explode()
				self.plane.explode()


if __name__ == '__main__':
	game = Game()
	game.run()