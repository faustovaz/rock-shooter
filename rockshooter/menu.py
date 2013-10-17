import pygame
import game

class Menu:
	def __init__(self):
		self.gameTitle = pygame.image.load("images/game_title.png").convert_alpha()
		self.playImages = self._loadPlayImages()
		self.recordsImages = self._loadRecordsImages()
		self.exitImages = self._loadExitImages()
		self.options = {"play" : True, "records" : False, "exit" : False}


	def _loadPlayImages(self):
		unselectedPlayImage = pygame.image.load("images/unselected_play.png").convert_alpha()
		selectedPlayImage = pygame.image.load("images/selected_play.png").convert_alpha()
		return { "selectedImage" : selectedPlayImage, "unselectedImage" : unselectedPlayImage}

	def _loadRecordsImages(self):
		unselectedRecordsImage = pygame.image.load("images/unselected_records.png").convert_alpha()
		selectedRecordsImage = pygame.image.load("images/selected_records.png").convert_alpha()
		return {"selectedImage" : selectedRecordsImage, "unselectedImage" : unselectedRecordsImage}

	def _loadExitImages(self):
		unselectedExitImage = pygame.image.load("images/unselected_exit.png").convert_alpha()
		selectedExitImage = pygame.image.load("images/selected_exit.png").convert_alpha()
		return {"selectedImage" : selectedExitImage, "unselectedImage" : unselectedExitImage}

	def draw(self):
		game.Game.screen.blit(self.gameTitle, (120, 50))
		self._drawOptionPlay()
		self._drawOptionRecords()
		self._drawOptionExit()

	def _drawOptionPlay(self):
		if self.options["play"]:
			game.Game.screen.blit(self.playImages['selectedImage'], (500, 240))
		else:
			game.Game.screen.blit(self.playImages['unselectedImage'], (500, 240))		

	def _drawOptionRecords(self):
		if self.options['records']:
			game.Game.screen.blit(self.recordsImages['selectedImage'], (500, 320))
		else:
			game.Game.screen.blit(self.recordsImages['unselectedImage'], (500, 320))

	def _drawOptionExit(self):
		if self.options['exit']:
			game.Game.screen.blit(self.exitImages['selectedImage'], (500, 410))
		else:
			game.Game.screen.blit(self.exitImages['unselectedImage'], (500, 410))

	def moveDown(self):
		if self.options['play']:
			self.options['records'] = True
			self.options['play'] = False
		elif self.options['records']:
			self.options['exit'] = True
			self.options['records'] = False

	def moveUp(self):
		if self.options['exit']:
			self.options['records'] = True
			self.options['exit'] = False
		elif self.options['records']:
			self.options['play'] = True
			self.options['records'] = False

	def _updateMenuOption(self):
		for index, option in enumerate(self.options):
			if index == self.selectedOption:
				self.options[option] = True
			else:
				self.options[option] = False