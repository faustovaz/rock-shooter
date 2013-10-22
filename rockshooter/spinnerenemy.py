import pygame
import enemy
import game

class SpinnerEnemy(enemy.Enemy):
	
	def __init__(self):
		enemy.Enemy.__init__(self)
		self.spriteIndex = 0
		self.sprites = self._getSpriteSequence()
		self.background = pygame.Surface((48, 50)).convert()

	def loadImage(self):
		self.image = pygame.image.load("images/enemy_1.png")		

	def getRect(self):
		return pygame.Rect(self.position[0], self.position[1], 48, 50)		

	def draw(self):
		if not self.toExplode:
			game.Game.screen.blit(self.sprites[self.spriteIndex], self.position)
			self.spriteIndex = self.spriteIndex + 1
			if self.spriteIndex > 3:
				self.spriteIndex = 0
		else:
			self.explodeMe()

	def move(self):
		if  self._isInsideScreen() and (not self.toExplode):
			self.position = (self.position[0], self.position[1] + 1)
			self.rect.left, self.rect.top = self.position
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