import pygame
import game
from bullet import Bullet

class AirCraft:

	def __init__(self):
		self.airCraftImage = pygame.image.load("images/aircraft.png")
		self.airCraftRect = self.airCraftImage.get_rect()
		self.airCraftPosition = (300, 400)
		self.airCraftExplosionImage = pygame.image.load("images/aircraft_explosion.png")
		self.airCraftExplosionSprites = self._loadExplosionSprites()
		self.airCraftExplosionSpritesIndex = 0
		self.exploded = False
		self.bullets = []
		self.toExplode = False
		self.exploded = False

	def draw(self):
		if not self.toExplode:
			self.airCraftRect.left, self.airCraftRect.top = self.airCraftPosition
			game.Game.screen.blit(self.airCraftImage, self.airCraftPosition)
		else:
			self.explodeMe()


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
		bullet = BulletAirCraft(self.airCraftPosition[0] + 30, self.airCraftPosition[1] - 10)
		bullet.draw()
		self.bullets.append(bullet)

	def updateBullets(self):
		self._removeUnvisibleBullets()
		for bullet in self.bullets:
			bullet.move()
			bullet.draw()

	def _removeUnvisibleBullets(self):
		visibleBullets = []
		for bullet in self.bullets:
			if bullet.isVisible():
				visibleBullets.append(bullet)
		self.bullets = visibleBullets		

	def _loadExplosionSprites(self):
		explosionSprites = []
		explosionClips = [
			[ 0,   0, 48, 48],
			[ 48,  0, 48, 48],
			[ 96,  0, 48, 48],
			[144,  0, 48, 48],
			[  0, 48, 48, 48],
			[ 48, 48, 48, 48],
			[ 96, 48, 48, 48],
			[144, 48, 48, 48],
		]
		for clip in explosionClips:
			self.airCraftExplosionImage.set_clip(pygame.Rect(clip[0], clip[1], clip[2], clip[3]))
			explosionSprites.append(self.airCraftExplosionImage.subsurface(self.airCraftExplosionImage.get_clip()))
		return explosionSprites		

	def explode(self):
		self.toExplode = True

	def explodeMe(self):
		if (self.airCraftExplosionSpritesIndex < 8):
			sprite = self.airCraftExplosionSprites[self.airCraftExplosionSpritesIndex]
			game.Game.screen.blit(sprite, self.airCraftPosition)
			self.airCraftExplosionSpritesIndex = self.airCraftExplosionSpritesIndex + 1
		else:
			self.exploded = True


class BulletAirCraft(Bullet):

	def __init__(self, x, y):
		Bullet.__init__(self, x, y)
		
	def loadImage(self):
		self.bulletImage = pygame.image.load("images/bullet.png").convert()		

	def move(self):
		bulletPositionY = self.bulletPosition[1] - 20;
		self.bulletPosition = (self.bulletPosition[0], bulletPositionY)
		self.rect.left, self.rect.top = self.bulletPosition
		if (bulletPositionY < 0):
			self.visible = False

	def getRect(self):
		self.rect = pygame.Rect(self.bulletPosition[0], self.bulletPosition[1], self.bulletImage.get_width(), self.bulletImage.get_height())					