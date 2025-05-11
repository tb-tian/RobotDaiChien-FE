import Const
import pygame

class PlayerStatus():
	def __init__(self, gameScreen, ID, isAlive, playerName, playerColor, statusCoord, statusLen):
		self.gameScreen = gameScreen
		self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
		self.playerName = playerName
		self.playerColor = playerColor
		self.statusCoord = statusCoord
		self.statusLen = statusLen
		self.playerID = ID
		self.playerScore = 0
		self.isAlive = isAlive
		# self.statusBackground = pygame.transform.scale(Const.STATUS_BACKGROUND, statusLen)
		
		# Avatar
		self.avaLen = statusLen[1] * 8 / 10
		self.playerAva = pygame.transform.scale(Const.PLAYER_AVA[self.playerID], (self.avaLen, self.avaLen))
		self.playerDeadAva = pygame.transform.scale(Const.PLAYER_AVA_DEAD[self.playerID], (self.avaLen, self.avaLen))
		self.skinCoord = (self.statusCoord[0] + self.statusLen[0] * 1 / 10, self.statusCoord[1] + (self.statusLen[1] - self.avaLen) / 2)
		
		if ID % 2 != 0:
			self.skinCoord = (self.statusCoord[0] + self.statusLen[0] - self.statusLen[0] * 1/ 10 - self.avaLen, self.statusCoord[1] + (self.statusLen[1] - self.avaLen) / 2)

		# Player Name
		playerNameFont = pygame.font.Font('Assets/Fonts/VCR_OSD_MONO.ttf', 25 * self.screenWidth // Const.DELL[0])
		self.playerNameText = playerNameFont.render(playerName, True, Const.PLAYER_COLOR_DICT[playerColor])
		playerNameHeight = playerNameFont.size(playerName)[1]
		playerNameWidth = playerNameFont.size(playerName)[0]
		self.playerNameCoord = (self.skinCoord[0] + self.avaLen + statusLen[0] * 1 / 30, self.skinCoord[1] + (self.avaLen - playerNameHeight) / 2)

		if ID % 2 != 0:
			self.playerNameCoord = (self.skinCoord[0] - playerNameWidth - statusLen[0] * 1 / 30, self.skinCoord[1] + (self.avaLen - playerNameHeight) / 2)

		# Score
		self.playerScoreFont = pygame.font.Font('Assets/Fonts/VCR_OSD_MONO.ttf', 35 * self.screenWidth // Const.DELL[0])
		self.playerScoreText = self.playerScoreFont.render(str(self.playerScore), True, Const.PLAYER_COLOR_DICT[playerColor])
		self.scoreHeight = self.playerScoreFont.size(str(self.playerScore))[1]
		self.scoreWidth = self.playerScoreFont.size(str(self.playerScore))[0]
		self.playerScoreCoord = (self.skinCoord[0] + (self.avaLen - self.scoreWidth) / 2, self.skinCoord[1] + self.avaLen + statusLen[1] * 1 / 30)

		if ID > 1:
			self.playerScoreCoord = (self.skinCoord[0] + (self.avaLen - self.scoreWidth) / 2, self.skinCoord[1] - self.scoreHeight - statusLen[1] * 1 / 30)

	def displayStatusImage(self):
		if self.isAlive == True:
			self.gameScreen.blit(self.playerAva, self.skinCoord)
		else:
			self.gameScreen.blit(self.playerDeadAva, self.skinCoord)

		self.gameScreen.blit(self.playerNameText, self.playerNameCoord)

		self.gameScreen.blit(self.playerScoreText, self.playerScoreCoord)

	def updateScore(self, curScore):
		self.playerScore = curScore
		self.playerScoreText = self.playerScoreFont.render(str(self.playerScore), True, Const.PLAYER_COLOR_DICT[self.playerColor])
		self.scoreHeight = self.playerScoreFont.size(str(self.playerScore))[1]
		self.scoreWidth = self.playerScoreFont.size(str(self.playerScore))[0]
		self.playerScoreCoord = (self.skinCoord[0] + (self.avaLen - self.scoreWidth) / 2, self.skinCoord[1] + self.avaLen + self.statusLen[1] * 1 / 30)

		if self.playerID > 1:
			self.playerScoreCoord = (self.skinCoord[0] + (self.avaLen - self.scoreWidth) / 2, self.skinCoord[1] - self.scoreHeight - self.statusLen[1] * 1 / 30)

	def updateAlive(self, isAlive):
		self.isAlive = isAlive

	def GetInfo(self):
		return (self.playerName, self.playerScore, self.playerColor, self.playerAva)

	