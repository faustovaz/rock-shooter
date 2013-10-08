import pygame
import game

class AirCraft:

	def __init__(self):
		self.airCraftImage = pygame.image.load("images/aircraft.png")
		self.airCraftRect = self.airCraftImage.get_rect()
		self.airCraftPosition = (300, 400)
		self.bullets = []

	def draw(self):
		game.Game.screen.blit(self.airCraftImage, self.airCraftPosition)

	def moveLeft(self):
		airCraftPositionX = self.airCraftPosition[0] - 5
		if (airCraftPositionX == 0):
			self.airCraftPosition = (0, self.airCraftPosition[1])
		else:
			self.airCraftPosition = (airCraftPositionX, self.airCraftPosition[1])

	def moveRight(self):
		airCraftPositionX = self.airCraftPosition[0] + 5
		if (airCraftPositionX == game.Game.screenSize[0]):
			self.airCraftPosition = (self.airCraftPosition[0], self.airCraftPosition[1])
		else:
			self.airCraftPosition = (airCraftPositionX, self.airCraftPosition[1])

	def moveUp(self):
		airCraftPositionY = self.airCraftPosition[1] - 5
		if (airCraftPositionY == game.Game.screenSize[1]):
			self.airCraftPosition = (self.airCraftPosition[0], self.airCraftPosition[1])
		else:
			self.airCraftPosition = (self.airCraftPosition[0], airCraftPositionY)

	def moveDown(self):
		airCraftPositionY = self.airCraftPosition[1] + 5
		if (airCraftPositionY == game.Game.screenSize[1]):
			self.airCraftPosition = (self.airCraftPosition[0], self.airCraftPosition[1])
		else:
			self.airCraftPosition = (self.airCraftPosition[0], airCraftPositionY)

	def shoot(self):
		bullet = Bullet(self.airCraftPosition[0] + 30, self.airCraftPosition[1] - 10)
		bullet.draw()
		self.bullets.append(bullet)

	def updateBullets(self):
		self._removeUnvisibleBullets()
		for bullet in self.bullets:
			bullet.move()
			bullet.draw()

	def _removeUnvisibleBullets(self):
		visibleBullets = []
		for index, bullet in enumerate(self.bullets):
			if bullet.isVisible():
				visibleBullets.append(bullet)
		self.bullets = visibleBullets		


class Bullet:

	def __init__(self, x, y):
		self.bulletImage = pygame.image.load("images/bullet.png").convert()
		self.bulletPosition = (x, y)
		self.visible = True

	def move(self):
		bulletPositionY = self.bulletPosition[1] - 20;
		self.bulletPosition = (self.bulletPosition[0], bulletPositionY)
		if (bulletPositionY < 0):
			self.visible = False	

	def draw(self):
		game.Game.screen.blit(self.bulletImage, self.bulletPosition)

	def isVisible(self):
		return self.visible