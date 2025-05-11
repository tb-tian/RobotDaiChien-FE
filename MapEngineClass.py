import pygame
import Const

class MapEngine():
	def __init__(self, gameScreen, engineCoord, engineSize, engineDir):
		self.gameScreen = gameScreen
		self.engineCoord = engineCoord
		self.engineSize = engineSize
		self.engineDir = engineDir

		self.engineFrame = []
		for frame in Const.GAME_BACKGROUND_ENGINE[self.engineDir]:
			self.engineFrame.append(pygame.transform.scale(frame, self.engineSize))

		self.curFrame = 0
		self.numFrame = len(self.engineFrame)

	def DisplayFrame(self):
		self.gameScreen.blit(self.engineFrame[self.curFrame], self.engineCoord)

	def MoveFrame(self):
		self.DisplayFrame()
		self.curFrame = (self.curFrame + 1) % self.numFrame
