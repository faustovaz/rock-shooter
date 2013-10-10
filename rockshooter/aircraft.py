import pygame
import game

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
			game.Game.screen.blit(self.airCraftImage, self.airCraftPosition)
			self.airCraftRect.top, self.airCraftRect.left = self.airCraftPosition
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


class Bullet:

	def __init__(self, x, y):
		self.bulletImage = pygame.image.load("images/bullet.png").convert()
		self.bulletPosition = (x, y)
		self.visible = True
		self.rect = pygame.Rect(x, y, self.bulletImage.get_width(), self.bulletImage.get_height())

	def move(self):
		bulletPositionY = self.bulletPosition[1] - 20;
		self.bulletPosition = (self.bulletPosition[0], bulletPositionY)
		self.rect.top, self.rect.left = self.bulletPosition
		if (bulletPositionY < 0):
			self.visible = False	

	def draw(self):
		game.Game.screen.blit(self.bulletImage, self.bulletPosition)

	def isVisible(self):
		return self.visible