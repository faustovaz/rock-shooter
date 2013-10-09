import pygame
import random
import game


class Enemy:

	def __init__(self):
		self.image = pygame.image.load("images/enemy_1.png")
		self.sprites = self._getSpriteSequence()
		self.spriteIndex = 0
		self.position = self.getRandomPosition()
		self.isVisible = True
		self.background = pygame.Surface((48, 50)).convert()
		self.explosionImage = pygame.image.load("images/enemy_explosion.png")
		self.explosionSprites = self._getExplosionSpriteSequence()

	def move(self):
		if (self.position[1] + 1 < game.Game.screenSize[1]):
			self.position = (self.position[0], self.position[1] + 1)
		else:
			self.isVisible = False

	def _getSpriteSequence(self):
		sprites = []
		clips = [ [0, 0, 48, 50], [48, 0, 48, 50], [96, 0, 48, 50], [144, 0, 48, 50] ]
		for clip in clips:
			self.image.set_clip(pygame.Rect(clip[0], clip[1],  clip[2], clip[3]))
			sprites.append(self.image.subsurface(self.image.get_clip()))
		return sprites

	def draw(self):
		game.Game.screen.blit(self.sprites[self.spriteIndex], self.position)
		self.spriteIndex = self.spriteIndex + 1
		if self.spriteIndex > 3:
			self.spriteIndex = 0

	def getRandomPosition(self):

		randomX = random.randint(10, game.Game.screenSize[0] - 10)
		return (randomX, 0)

	def explode(self):
		pass

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
			explosionSprites.append(self.explosionImages.subsurface(self.image.get_clip()))
		return explosionSprites