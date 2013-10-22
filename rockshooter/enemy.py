import pygame
import random
import game
from executiontime import ExecutionTime


class Enemy:

	def __init__(self):
		self.loadImage()
		self.position = self.getRandomPosition()
		self.visible = True
		self.toExplode = False
		self.exploded = False
		self.explosionImage = pygame.image.load("images/enemy_explosion.png")
		self.explosionSprites = self._getExplosionSpriteSequence()
		self._rect = None
		self.spriteExplosionIndex = 0
		self.bullets = []

	def loadImage(self):
		pass
	
	def _isInsideScreen(self):
		return (self.position[1] + 1 < game.Game.screenSize[1])

	def move(self):
		pass

	def draw(self):
		pass

	def shoot(self):
		pass

	def moveBullets(self):
		pass

	@property
	def rect(self):
		if not self._rect:
			self._rect = self.getRect()
		return self._rect

	def getRect(self):
		pass

	def getRandomPosition(self):
		randomX = random.randint(50, game.Game.screenSize[0] - 50)
		return (randomX, 0)

	def explodeMe(self):
		game.Game.screen.blit(self.explosionSprites[self.spriteExplosionIndex], self.position)
		self.spriteExplosionIndex = self.spriteExplosionIndex + 1
		if self.spriteExplosionIndex > 7:
			self.spriteExplosionIndex = 0
			self.visible = False
			self.exploded = True

	def explode(self):
		self.toExplode = True

	def _getExplosionSpriteSequence(self):
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
			self.explosionImage.set_clip(pygame.Rect(clip[0], clip[1], clip[2], clip[3]))
			explosionSprites.append(self.explosionImage.subsurface(self.explosionImage.get_clip()))
		return explosionSprites