import pygame
import random
import game


class Enemy:

	def __init__(self):
		self.image = pygame.image.load("images/enemy_1.png")
		self.sprites = self._getSpriteSequence()
		self.spriteIndex = 0
		self.position = self.getRandomPosition()
		self.visible = True
		self.background = pygame.Surface((48, 50)).convert()
		self.toExplode = False
		self.exploded = False
		self.explosionTime = 0
		self.explosionImage = pygame.image.load("images/enemy_explosion.png")
		self.explosionSprites = self._getExplosionSpriteSequence()
		self.rect = pygame.Rect(self.position[0], self.position[1], 48, 50)
		self.spriteExplosionIndex = 0
		self.exploded = False

	def _isInsideScreen(self):
		return (self.position[1] + 1 < game.Game.screenSize[1])

	def move(self):
		if  self._isInsideScreen() and (not self.toExplode):
			self.position = (self.position[0], self.position[1] + 1)
			self.rect.top, self.rect.left = self.position
		else:
			if not self._isInsideScreen():
				self.visible = False

	def _getSpriteSequence(self):
		sprites = []
		clips = [ [0, 0, 48, 50], [48, 0, 48, 50], [96, 0, 48, 50], [144, 0, 48, 50] ]
		for clip in clips:
			self.image.set_clip(pygame.Rect(clip[0], clip[1],  clip[2], clip[3]))
			sprites.append(self.image.subsurface(self.image.get_clip()))
		return sprites

	def draw(self):
		if not self.toExplode:
			game.Game.screen.blit(self.sprites[self.spriteIndex], self.position)
			self.spriteIndex = self.spriteIndex + 1
			if self.spriteIndex > 3:
				self.spriteIndex = 0
		else:
			self.explodeMe()

	def getRandomPosition(self):
		randomX = random.randint(50, game.Game.screenSize[0] - 50)
		return (randomX, 0)

	def explodeMe(self):
		if self.explosionTime == 0:
			self.explosionTime = 2
			game.Game.screen.blit(self.explosionSprites[self.spriteExplosionIndex], self.position)
			self.spriteExplosionIndex = self.spriteExplosionIndex + 1
			if self.spriteExplosionIndex > 7:
				self.spriteExplosionIndex = 0
				self.visible = False
				self.exploded = True
		else:
			self.explosionTime = self.explosionTime - 1

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