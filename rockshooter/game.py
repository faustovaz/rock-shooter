import pygame
import sys
from pygame.locals import *
import aircraft
import random
import spinnerenemy
import robotenemy
from executiontime import ExecutionTime
import menu
import gamerecords

class Game:

	screenSize 	= (800, 600)
	screen 		= pygame.display.set_mode(screenSize)
	clock 		= pygame.time.Clock()
	timeTick 	= 100

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Rock shooter - v-1.0")
		self._loadImages()
		self._loadClouds()
		self._defineImagesPosition()
		self._loadFonts()
		self._prepareObjectsForANewGame()


	def _loadImages(self):
		self.firstBackgroundImage = pygame.image.load("images/background.png").convert_alpha()
		self.secondBackgroundImage = pygame.image.load("images/background.png").convert_alpha()
		self.cloudBackgroundImage = pygame.image.load("images/clouds.png").convert_alpha()
		self.gameOverImage = pygame.image.load("images/gameover.png").convert_alpha()

	def _loadClouds(self):
		self.clouds = []
		self.clouds.append(pygame.image.load("images/clouds.png").convert_alpha())
		self.clouds.append(pygame.image.load("images/clouds1.png").convert_alpha())
		self.clouds.append(pygame.image.load("images/clouds2.png").convert_alpha())


	def _defineImagesPosition(self):
		self.firstBackgroundPosition = (0, 0) 
		self.secondBackgroundPosition = (0, (-1) * Game.screenSize[1])
		self.cloudBackgroundPosition = (0, (-1) * self.cloudBackgroundImage.get_height())				


	def _loadFonts(self):
		self.recordFont = pygame.font.Font("fonts/28DaysLater.ttf", 50)
		self.enterYourNameFont = pygame.font.Font("fonts/disinteg.ttf", 50)


	def _prepareObjectsForANewGame(self):
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
			self.cloudBackgroundImage = self.clouds[random.randint(0, 2)]
		self.cloudBackgroundPosition = (cloudImagePositionX, cloudImagePositionY)
		Game.screen.blit(self.cloudBackgroundImage, self.cloudBackgroundPosition)


	def run(self):
		if self.plane.exploded:
			self._prepareObjectsForANewGame()
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
			self.updateDisplay()
			Game.clock.tick(Game.timeTick)
		self.gameOver()


	def updateDisplay(self):
		pygame.display.flip()


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
					self.quit()
				elif event.type == KEYDOWN:
					if event.key == K_SPACE:
						self.plane.shoot()


	def updateEnemies(self):
		visibleEnemies = []
		for enemy in self.enemies:	
			if enemy.visible and not enemy.exploded:
				enemy.move()
				enemy.shoot()
				enemy.moveBullets()
				enemy.draw()
				visibleEnemies.append(enemy)
		self.enemies = visibleEnemies
	

	@ExecutionTime(25)
	def _generateEnemies(self):
		self.enemies.append(spinnerenemy.SpinnerEnemy())
		if (random.randint(0,10) > 9):
			self.enemies.append(robotenemy.RobotEnemy())


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
			if len(enemy.bullets):
				for bullet in enemy.bullets:
					if bullet.visible and bullet.rect.colliderect(self.plane.airCraftRect) and not self.plane.toExplode:
						bullet.visible = False
						self.plane.explode()	


	def runMenu(self):
		gameMenu = menu.Menu()
		keepShowingMenu = True
		while keepShowingMenu:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quit()
				elif event.type == KEYDOWN:
					if event.key == K_UP:
						gameMenu.moveUp()
					elif event.key == K_DOWN:
						gameMenu.moveDown()
					elif event.key == K_RETURN:
						keepShowingMenu = False
			self._scrollBackground()
			self._showSomeClouds()
			gameMenu.draw()
			self.updateDisplay()
			Game.clock.tick(Game.timeTick)
		self._handleChosenOption(gameMenu.options)


	def _handleChosenOption(self, options):
		if options['play']:
			self.run()
		elif options['records']:
			self.showRecords()
		elif options['exit']:
			self.quit()


	def showRecords(self):
		keepShowingRecords = True
		recordsReadyToDisplay = self.getPlayersRecords()
		while keepShowingRecords:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quit()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						keepShowingRecords = False
			self._scrollBackground()
			self._showSomeClouds()
			self._drawRecordTitle()
			self._drawPlayersRecords(recordsReadyToDisplay)
			self.updateDisplay()
			Game.clock.tick(Game.timeTick)
		self.runMenu()


	def getPlayersRecords(self):
		jumpFactor = 0
		recordsReadyToDisplay = []
		orderedKeys = sorted(gamerecords.records, key=gamerecords.records.get, reverse=True)
		for key in orderedKeys:
			player = self.recordFont.render(str(key), False, (255, 255, 255))
			points = self.recordFont.render(str(gamerecords.records.get(key)), False, (255, 255, 255))
			recordsReadyToDisplay.append(
				{	"player" : player, 
					"points" : points, 
					"playerPosition" : (260, 150 + jumpFactor), 
					"pointsPosition" : (440, 150 + jumpFactor)
				}
			)
			jumpFactor = jumpFactor + 60	
		return recordsReadyToDisplay	


	def _drawPlayersRecords(self, records):
		for recordToDisplay in records:
			Game.screen.blit(recordToDisplay['player'], recordToDisplay['playerPosition'])
			Game.screen.blit(recordToDisplay['points'], recordToDisplay['pointsPosition'])		


	def _drawRecordTitle(self):
		recordTitle = self.recordFont.render("Records", False, (255, 255, 255))
		Game.screen.blit(recordTitle, (330, 50))		


	def gameOver(self):
		keepShowingGameOverMessage = True
		while keepShowingGameOverMessage:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quit()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						keepShowingGameOverMessage = False
			self._scrollBackground()
			self._showSomeClouds()
			self._drawGameOverMessage()
			self.updateDisplay()
			Game.clock.tick(Game.timeTick)
		if self.shouldInsertANewRecord():
			self.readPlayerName()
		self.runMenu()


	def _drawGameOverMessage(self):
		Game.screen.blit(self.gameOverImage, (170, 160))		


	def isANewRecord(self):
		for key, value in gamerecords.records.iteritems():
			if self.scores > value:
				return True
		return False


	def shouldInsertANewRecord(self):
		return (self.isANewRecord() or len(gamerecords.records) < 5)


	def readPlayerName(self):
		message = self.enterYourNameFont.render("Type your name: ", True, (255, 255, 255))
		keepWaitingForThePlayerName = True
		name = ""
		playerName = None
		while keepWaitingForThePlayerName:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quit()
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
					else:
						key = event.key
						if (97 <= key <= 122) and len(name) < 3: #Read just 3 chars and chars between a-z
							name = name + chr(key)
			playerName = self.enterYourNameFont.render(name, False, (255, 255, 255))
			self._scrollBackground()
			self._showSomeClouds()
			self._drawGameOverMessage()
			Game.screen.blit(message, (170, 290))
			Game.screen.blit(playerName, (500, 290))
			self.updateDisplay()
			Game.clock.tick(Game.timeTick)


	def updateRecords(self, name):
		if len(gamerecords.records) < 5:
			gamerecords.records.update({name : self.scores})
		else:
			orderedKeys = sorted(gamerecords.records, key=gamerecords.records.get, reverse=False)
			gamerecords.records.pop(orderedKeys[0])
			gamerecords.records.update({str(name) : self.scores})
		with open("rockshooter/gamerecords.py", "w") as recordFile:
			recordFile.write('records = ' + str(gamerecords.records))


	def quit(self):
		pygame.quit()
		sys.exit()		