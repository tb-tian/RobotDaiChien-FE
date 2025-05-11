import pygame
import Const
import CellClass

class Portal():
	def __init__(self, gameScreen, curCell):
		self.gameScreen = gameScreen
		self.portalCell = curCell
		self.portalCoord = self.portalCell.GetPos()
		self.portalFrameHeight = self.portalCell.GetLen() / 6 * 7
		self.portalFrameWidth = self.portalFrameHeight
		self.portalPadding = ((self.portalCell.GetLen() - self.portalFrameWidth) / 2, (self.portalCell.GetLen() - self.portalFrameHeight) / 2) 

		self.portalFrame = []
		for frame in Const.PORTAL_FRAME_LIST:
			self.portalFrame.append(pygame.transform.scale(frame, (self.portalFrameWidth, self.portalFrameHeight)))

		self.curFrame = 0
		self.numFrame = len(self.portalFrame)

	def DisplayFrame(self):
		self.gameScreen.blit(self.portalFrame[self.curFrame], (self.portalCoord[0] + self.portalPadding[0], self.portalCoord[1] + self.portalPadding[1]))

	def MoveFrame(self):
		self.DisplayFrame()
		self.curFrame = (self.curFrame + 1) % self.numFrame
