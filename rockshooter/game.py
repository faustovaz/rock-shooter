import pygame
import sys
from pygame.locals import *
import aircraft
import random
import enemy
from executiontime import ExecutionTime
import menu
import records

class Game:

	screenSize 	= (800, 600)
	screen 		= pygame.display.set_mode(screenSize)
	clock 		= pygame.time.Clock()
	timeTick 	= 100

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Rock shooter - v-1.0")
		self._loadAssets()

	def _loadAssets(self):
		self.firstBackgroundImage = pygame.image.load("images/background.png").convert_alpha()
		self.secondBackgroundImage = pygame.image.load("images/background.png").convert_alpha()
		self.cloudBackgroundImage = pygame.image.load("images/clouds.png").convert_alpha()
		self.gameOverImage = pygame.image.load("images/gameover.png").convert_alpha()
		self.firstBackgroundPosition = (0, 0) 
		self.secondBackgroundPosition = (0, (-1) * Game.screenSize[1])
		self.cloudBackgroundPosition = (0, (-1) * self.cloudBackgroundImage.get_height())
		self.plane = aircraft.AirCraft()
		self.enemies = []		
		self.scores = 0

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
		if self.plane.exploded:
			self._loadAssets()
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
		self.gameOver()

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
					self.scores = self.scores + 10

	def checkHitPlayer(self):
		for enemy in self.enemies:
			if enemy.visible and self.plane.airCraftRect.colliderect(enemy.rect) and not self.plane.toExplode:
				enemy.explode()
				self.plane.explode()

	def runMenu(self):
		gameMenu = menu.Menu()
		choosenOption = False
		while not choosenOption:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_UP:
						gameMenu.moveUp()
					elif event.key == K_DOWN:
						gameMenu.moveDown()
					elif event.key == K_RETURN:
						self._handleChosenOption(gameMenu.options)
			self._scrollBackground()
			self._showSomeClouds()
			gameMenu.draw()
			pygame.display.flip()
			Game.clock.tick(Game.timeTick)


	def _handleChosenOption(self, options):
		if options['play']:
			self.run()
		elif options['records']:
			self.showRecords()
		elif options['exit']:
			pygame.quit()
			sys.exit()

	def showRecords(self):
		recordFont = pygame.font.Font("fonts/28DaysLater.ttf", 50)
		factor = 0
		keepShowingRecords = True
		recordsReadyToDisplay = []
		recordTitle = recordFont.render("Records", False, (255, 255, 255))
		orderedKeys = sorted(records.records, key=records.records.get, reverse=True)
		for key in orderedKeys:
			player = recordFont.render(str(key), False, (255, 255, 255))
			points = recordFont.render(str(records.records.get(key)), False, (255, 255, 255))
			recordsReadyToDisplay.append(
					{	"player" : player, 
						"points" : points, 
						"playerPosition" : (260, 150 + factor),
						"pointsPosition" : (440, 150 + factor)
					}
			)
			factor = factor + 60
		while keepShowingRecords:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						keepShowingRecords = False
			self._scrollBackground()
			Game.screen.blit(recordTitle, (330, 50))
			for recordToDisplay in recordsReadyToDisplay:
				Game.screen.blit(recordToDisplay['player'], recordToDisplay['playerPosition'])
				Game.screen.blit(recordToDisplay['points'], recordToDisplay['pointsPosition'])
			pygame.display.flip()
			Game.clock.tick(Game.timeTick)
		self.runMenu()

	def gameOver(self):
		keepShowingGameOverMessage = True
		while keepShowingGameOverMessage:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						keepShowingGameOverMessage = False
			self._scrollBackground()
			self._showSomeClouds()
			Game.screen.blit(self.gameOverImage, (170, 160))
			pygame.display.flip()
			Game.clock.tick(Game.timeTick)
		if self.isANewRecord() or len(records.records) < 5:
			self.showTypeYourNameMessage()
			self.readPlayerName()
		self.runMenu()

	def isANewRecord(self):
		for key, value in records.records.iteritems():
			if self.scores > value:
				return True
		return False

	def showTypeYourNameMessage(self):
		pass

	def readPlayerName(self):
		font = pygame.font.Font("fonts/disinteg.ttf", 50)
		message = font.render("Type your name: ", True, (255, 255, 255))
		keepWaitingForThePlayerName = True
		name = ""
		playerName = None
		while keepWaitingForThePlayerName:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						keepWaitingForThePlayerName = False
					elif event.key == K_RETURN:
						if len(name):
							self.updateRecords(name)
							keepWaitingForThePlayerName = False
						else:
							keepWaitingForThePlayerName = False
					elif event.key == K_BACKSPACE:
						if len(name) > 0:
							name = name[0:len(name) - 1]
							playerName = font.render(name, False, (255, 255, 255))
					else:
						key = event.key
						if (26 < key < 126) and len(name) < 3:
							name = name + chr(key)
							playerName = font.render(name, False, (255, 255, 255))

			self._scrollBackground()
			Game.screen.blit(self.gameOverImage, (170, 160))
			Game.screen.blit(message, (170, 290))
			if playerName:
				Game.screen.blit(playerName, (500, 290))
			pygame.display.flip()
			Game.clock.tick(Game.timeTick)

	def updateRecords(self, name):
		if len(records.records) < 5:
			records.records.update({name : self.scores})
		else:
			orderedRecords = {}
			orderedKeys = sorted(records.records, key=records.records.get, reverse=False)
			records.records.pop(orderedKeys[0])
			records.records.update({str(name) : self.scores})
		with open("rockshooter/records.py", "w") as recordFile:
			recordFile.write('records = ' + str(records.records))