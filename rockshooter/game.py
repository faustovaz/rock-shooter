import pygame
import sys
from pygame.locals import *
import aircraft
import random
import enemy
from executiontime import ExecutionTime

class Game:

	screenSize 	= (800, 600)
	screen 		= pygame.display.set_mode(screenSize)
	clock 		= pygame.time.Clock()
	timeTick 	= 100

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Rock shooter - v-1.0")
		self.firstBackgroundImage = pygame.image.load("images/background.png").convert_alpha()
		self.secondBackgroundImage = pygame.image.load("images/background.png").convert_alpha()
		self.cloudBackgroundImage = pygame.image.load("images/clouds.png").convert_alpha()
		self.firstBackgroundPosition = (0, 0) 
		self.secondBackgroundPosition = (0, (-1) * Game.screenSize[1])
		self.cloudBackgroundPosition = (0, (-1) * self.cloudBackgroundImage.get_height())
		self.plane = aircraft.AirCraft()
		self.enemies = []

	def _scrollBackground(self):
		firstImageX, firstImageY = self.firstBackgroundPosition
		secondImageX, secondImageY = self.secondBackgroundPosition
		firstImageY = firstImageY + 2
		if (firstImageY > Game.screenSize[1]):
			firstImageY = (Game.screenSize[1] * (-1)) + 2
		secondImageY = secondImageY + 2
		if (secondImageY > Game.screenSize[1]):
			secondImageY = (Game.screenSize[1] * (-1)) + 2
		self.firstBackgroundPosition = (0, firstImageY)
		self.secondBackgroundPosition = (0, secondImageY)
		Game.screen.blit(self.firstBackgroundImage, self.firstBackgroundPosition)
		Game.screen.blit(self.secondBackgroundImage, self.secondBackgroundPosition)

	def _showSomeClouds(self):	
		cloudImagePositionX, cloudImagePositionY = self.cloudBackgroundPosition
		cloudImagePositionY = cloudImagePositionY + 3
		if (cloudImagePositionY > Game.screenSize[1]):
			cloudImagePositionY = (-1) * self.cloudBackgroundImage.get_height()
		self.cloudBackgroundPosition = (cloudImagePositionX, cloudImagePositionY)
		Game.screen.blit(self.cloudBackgroundImage, self.cloudBackgroundPosition)

	def run(self):
		while not self.plane.exploded:
			self._handleEvents()
			self._scrollBackground()
			self._showSomeClouds()
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
	
	@ExecutionTime(25)
	def _generateEnemies(self):
		self.enemies.append(enemy.Enemy())

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

	def runMenu(self):
		menu = Menu()
		choosenOption = False
		while not choosenOption:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_UP:
						pass
					elif event.key == K_DOWN:
						pass
			self._scrollBackground()
			self._showSomeClouds()
			menu.draw()
			pygame.display.flip()
			Game.clock.tick(Game.timeTick)

class Menu:
	def __init__(self):
		self.gameTitle = pygame.image.load("images/game_title.png").convert_alpha()
		self.playImages = self._loadPlayImages()
		self.recordsImages = self._loadRecordsImages()
		self.exitImages = self._loadExitImages()
		self.options = {"play" : True, "records" : False, "exit"	: False}


	def _loadPlayImages(self):
		unselectedPlayImage = pygame.image.load("images/unselected_play.png").convert_alpha()
		selectedPlayImage = pygame.image.load("images/selected_play.png").convert_alpha()
		return { "selectedImage" : selectedPlayImage, "unselectedImage" : unselectedPlayImage}

	def _loadRecordsImages(self):
		unselectedRecordsImage = pygame.image.load("images/unselected_records.png").convert_alpha()
		selectedRecordsImage = pygame.image.load("images/selected_records.png").convert_alpha()
		return {"selectedImage" : selectedRecordsImage, "unselectedImage" : unselectedRecordsImage}

	def _loadExitImages(self):
		unselectedExitImage = pygame.image.load("images/unselected_exit.png").convert_alpha()
		selectedExitImage = pygame.image.load("images/selected_exit.png").convert_alpha()
		return {"selectedImage" : selectedExitImage, "unselectedImage" : unselectedExitImage}

	def draw(self):
		Game.screen.blit(self.gameTitle, (120, 50))
		self._drawOptionPlay()
		self._drawOptionRecords()
		self._drawOptionExit()

	def _drawOptionPlay(self):
		if self.options["play"]:
			Game.screen.blit(self.playImages['selectedImage'], (500, 240))
		else:
			Game.screen.blit(self.playImages['unselectedImage'], (500, 240))		

	def _drawOptionRecords(self):
		if self.options['records']:
			Game.screen.blit(self.recordsImages['selectedImage'], (500, 320))
		else:
			Game.screen.blit(self.recordsImages['unselectedImage'], (500, 320))

	def _drawOptionExit(self):
		if self.options['exit']:
			Game.screen.blit(self.exitImages['selectedImage'], (500, 410))
		else:
			Game.screen.blit(self.exitImages['unselectedImage'], (500, 410))

	def moveDown(self):
		pass

	def moveUp(self):
		pass
