import pygame
import game

class Bullet:

	def __init__(self, x, y):
		self.bulletImage = None
		self.loadImage()
		self.bulletPosition = (x, y)
		self.visible = True
		self.getRect()

	def loadImage(self):
		pass		

	def move(self):
		bulletPositionY = self.bulletPosition[1] + 10;
		self.bulletPosition = (self.bulletPosition[0], bulletPositionY)
		self.rect.left, self.rect.top = self.bulletPosition
		if (bulletPositionY > game.Game.screenSize[1]):
			self.visible = False	

	def draw(self):
		game.Game.screen.blit(self.bulletImage, self.bulletPosition)

	def isVisible(self):
		return self.visible

	def getRect(self):
		pass