import game
import enemy
import pygame
from executiontime import ExecutionTime
from bullet import Bullet
import random


class RobotEnemy(enemy.Enemy):

	def __init__(self):
		enemy.Enemy.__init__(self)
		self.direction = "moveLeft"

	def loadImage(self):
		self.image = pygame.image.load("images/enemy_2.png").convert_alpha()

	def getRect(self):
		return pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())

	def draw(self):
		if not self.toExplode:
			game.Game.screen.blit(self.image, self.position)
		else:
			self.explodeMe()		

	def move(self):
		if  self._isInsideScreen() and (not self.toExplode):
			if (random.randint(0, 10) > 7):
				self.position = (self.position[0], self.position[1] + 1)
			else:
				if self.direction == "moveLeft":
					self.position = (self.position[0] - 1, self.position[1])
					if self.position[0] == 0:
						self.direction = "moveRight"
				elif self.direction == "moveRight":
					self.position = (self.position[0] + 1, self.position[1])
					if (self.position[1] + self.image.get_width()) == game.Game.screenSize[1]:
						self.direction = "moveLeft"
			self.rect.left, self.rect.top = self.position
		else:
			if not self._isInsideScreen():
				self.visible = False

	def moveBullets(self):
		for bullet in self.bullets:
			bullet.move()
			bullet.draw()

	@ExecutionTime(50)
	def shoot(self):
		bulletRight = BulletEnemy(self.position[0] + 25, self.position[1] + self.image.get_height() + 5)
		bulletLeft = BulletEnemy(self.position[0] + 85, self.position[1] + self.image.get_height() + 5)
		bulletRight.draw()
		bulletLeft.draw()
		self.bullets.append(bulletRight)
		self.bullets.append(bulletLeft)


class BulletEnemy(Bullet):

	def __init__(self, x, y):
		Bullet.__init__(self, x, y)

	def loadImage(self):
		self.bulletImage = pygame.image.load("images/enemy_2_bullet.png").convert_alpha()		

	def move(self):
		bulletPositionY = self.bulletPosition[1] + 10;
		self.bulletPosition = (self.bulletPosition[0], bulletPositionY)
		self.rect.left, self.rect.top = self.bulletPosition
		if (bulletPositionY > game.Game.screenSize[1]):
			self.visible = False	

	def getRect(self):
		self.rect = pygame.Rect(self.bulletPosition[0], self.bulletPosition[1], self.bulletImage.get_width(), self.bulletImage.get_height())		