import pygame
import Const

class Cell():
	def __init__(self, cellCoord, cellIndex, cellLen):
		self.cellLen = cellLen
		self.cellCoord = cellCoord
		self.cellIndex = cellIndex
		self.listAdj = [None, None, None, None]
		self.move = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
		self.playerSet = set()

	def AddPlayer(self, playerId):
		self.playerSet.add(playerId)

	def RemovePlayer(self, playerId):
		if playerId in self.playerSet:
			self.playerSet.discard(playerId)

	def AddAdj(self, adjCell, pos):
		if pos < 0 or pos > 3:
			return
		self.listAdj[pos] = adjCell

	def GetCellIndex(self):
		return self.cellIndex

	def GetPlayerPos(self, playerId):
		if len(self.playerSet) <= 1:
			return self.cellCoord
		return (self.cellCoord[0] + self.move[playerId][0] * self.cellLen / 5, self.cellCoord[1] + self.move[playerId][1] * self.cellLen / 5)

	def GetPos(self):
		return self.cellCoord

	def GetAdj(self, pos):
		if pos < 0 or pos > 3:
			return None
		return self.listAdj[pos]

	def GetLen(self):
		return self.cellLen

class ObstacleCell(Cell):
	def __init__(self, gameScreen, cellCoord, cellIndex, cellLen):
		Cell.__init__(self, cellCoord, cellIndex, cellLen)

		self.gameScreen = gameScreen
		self.backgroundImage = [
			pygame.transform.scale(Const.CELL_IMAGE_LIST[10], (cellLen, cellLen)),
			pygame.transform.scale(Const.CELL_IMAGE_LIST[11], (cellLen, cellLen))
		]
		self.cellColor = 0

	def DisplayBackgroundImage(self):
		self.gameScreen.blit(self.backgroundImage[self.cellColor], self.cellCoord)

	def LockCell(self):
		self.cellColor = 1

class EmptyCell(Cell):
	def __init__(self, gameScreen, cellCoord, cellIndex, cellLen, cellColor):
		Cell.__init__(self, cellCoord, cellIndex, cellLen)

		self.gameScreen = gameScreen
		self.cellColor = cellColor
		self.isLocked = False
		self.backgroundImage = [
			pygame.transform.scale(Const.CELL_IMAGE_LIST[i], (cellLen, cellLen)) for i in range(10)
		]

	def DisplayBackgroundImage(self):
		self.gameScreen.blit(self.backgroundImage[self.cellColor], self.cellCoord)
		# if self.isLocked:
		# 	self.gameScreen.blit(self.backgroundImage[5], self.cellCoord)

	def ChangeCellColor(self, newColor):
		self.cellColor = newColor

	def LockCell(self):
		self.cellColor = 5

class TangTocCell(Cell):
	def __init__(self, gameScreen, cellCoord, cellIndex, cellLen):
		Cell.__init__(self, cellCoord, cellIndex, cellLen)

		self.gameScreen = gameScreen
		self.isLocked = False
		self.backgroundImage = pygame.transform.scale(Const.TANG_TOC, (cellLen, cellLen))
		

	def DisplayBackgroundImage(self):
		self.gameScreen.blit(self.backgroundImage, self.cellCoord)

class MauNoCell(Cell):
	def __init__(self, gameScreen, cellCoord, cellIndex, cellLen):
		Cell.__init__(self, cellCoord, cellIndex, cellLen)

		self.gameScreen = gameScreen
		self.isLocked = False
		self.backgroundImage = pygame.transform.scale(Const.MAU_NO, (cellLen, cellLen))
		

	def DisplayBackgroundImage(self):
		self.gameScreen.blit(self.backgroundImage, self.cellCoord)

class DauTronCell(Cell):
	def __init__(self, gameScreen, cellCoord, cellIndex, cellLen):
		Cell.__init__(self, cellCoord, cellIndex, cellLen)

		self.gameScreen = gameScreen
		self.isLocked = False
		self.backgroundImage = pygame.transform.scale(Const.DAU_TRON, (cellLen, cellLen))
		

	def DisplayBackgroundImage(self):
		self.gameScreen.blit(self.backgroundImage, self.cellCoord)