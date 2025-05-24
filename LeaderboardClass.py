import os
import pygame
import Const
import PlayerClass
import ButtonClass
import MenuClass

class LeaderboardInfo():
	def __init__(self, gameScreen, containerSize, containerCoord, containerPadding, player, rank):
		self.gameScreen = gameScreen
		self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
		self.containerSize = containerSize
		self.containerCoord = containerCoord
		self.containerPadding = containerPadding
		self.containerRect = pygame.Rect(self.containerCoord[0] + self.containerPadding, self.containerCoord[1] + self.containerPadding, self.containerSize[0] - self.containerPadding * 2, self.containerSize[1] - self.containerPadding * 2)
		
		# self.playerInfoCoord = [name, score, rank, rank_image]
		self.rectPadding = 10
		self.rectContent = (self.containerRect.left + self.rectPadding, self.containerRect.top + self.rectPadding, self.containerRect.width - 2 * self.rectPadding, self.containerRect.height - 2 * self.rectPadding)
		
		self.player = player
		self.playerInfo = self.player.GetInfo()

		# Font
		self.scoreFont = pygame.font.Font('Assets/Fonts/VCR_OSD_MONO.ttf', 65 * self.screenWidth // Const.MSI[0])
		self.nameFont = pygame.font.Font('Assets/Fonts/AmaticSC-Bold.ttf', 55 * self.screenWidth // Const.MSI[0])

		# Player Ava
		self.playerAvaSize = (self.containerRect[1] * 4 / 5, self.containerRect[1] * 4 / 5)
		self.playerAva = pygame.transform.scale(self.playerInfo[3], self.playerAvaSize)
		self.playerAvaCoord = (self.rectContent[0] + (self.rectContent[2] - self.playerAvaSize[0]) / 2, self.rectContent[1] + (self.rectContent[3] - self.playerAvaSize[1]) / 2)

		# Player Cup
		self.playerRank = rank
		self.playerCup = pygame.transform.scale(Const.RANK_CUP[self.playerRank - 1], (50 * self.screenHeight / Const.MSI[1], 80 * self.screenHeight / Const.MSI[1]))

	def Display(self):
		pygame.draw.rect(self.gameScreen, Const.WHITE, self.containerRect, border_radius = 15)
		
		self.gameScreen.blit(self.playerAva, self.playerAvaCoord)

		# Name
		nameText = self.nameFont.render(self.playerInfo[0], True, Const.BLACK)
		nameWidth = self.nameFont.size(self.playerInfo[0])[0]
		nameHeight = self.nameFont.size(self.playerInfo[0])[1]
		self.gameScreen.blit(nameText, (self.rectContent[0] + (self.rectContent[2] - nameWidth) / 2, self.rectContent[1] + (self.playerAvaCoord[1] - self.rectContent[1] - nameHeight) / 2))

		# Score
		scoreText = self.scoreFont.render(str(self.playerInfo[1]), True, Const.BLACK)
		scoreWidth = self.scoreFont.size(str(self.playerInfo[1]))[0]
		scoreHeight = self.scoreFont.size(str(self.playerInfo[1]))[1]
		self.gameScreen.blit(scoreText, (self.rectContent[0] + (self.rectContent[2] - scoreWidth) / 2, self.playerAvaCoord[1] + self.playerAvaSize[1] + (self.rectContent[1] + self.rectContent[3] - self.playerAvaCoord[1] - self.playerAvaSize[1]  - nameHeight) / 2))

		self.gameScreen.blit(self.playerCup, (self.rectContent[0] + (self.rectContent[2] - self.playerCup.get_width()) / 2, self.rectContent[1] + self.rectContent[3] + self.rectPadding))


class Leaderboard():
	def __init__(self, playerList):
		# Screen
		if os.name == 'nt': 
			self.gameScreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		else:
			self.gameScreen = pygame.display.set_mode((1920, 1080))
		self.background = pygame.transform.scale(Const.LEADERBOARD_BG, (pygame.display.get_surface().get_size()))
		self.gameScreen.blit(self.background, (0, 0))
		self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()

		self.playerList = playerList
		self.playerContainerNum = len(self.playerList)
		
		# Set up game
		self.running = True
		self.clock = pygame.time.Clock()

		# sort
		for i in range(self.playerContainerNum):
			for j in range(i + 1, self.playerContainerNum):
				if self.playerList[i].GetInfo()[1] < self.playerList[j].GetInfo()[1]:
					self.playerList[i], self.playerList[j] = self.playerList[j], self.playerList[i]

		# Container
		self.playerContainerSize = (self.screenWidth / 4, self.screenHeight * 6 / 10)
		self.playerContainerPadding = self.playerContainerSize[0] * 1.5 / 10

		playerContainerInitCoord = ((self.screenWidth - self.playerContainerSize[0] * self.playerContainerNum) / 2, (self.screenHeight - self.playerContainerSize[1]) / 2)
		self.playerContainer = []
		for i in range(self.playerContainerNum):
			playerContainerCoord = ((playerContainerInitCoord[0] + i * self.playerContainerSize[0], playerContainerInitCoord[1]))
			self.playerContainer.append(LeaderboardInfo(self.gameScreen, self.playerContainerSize, playerContainerCoord, self.playerContainerPadding, self.playerList[i], i + 1))

		# Back Button
		self.backButtonSize = (self.screenWidth * 1 / 10, self.screenHeight * 1 / 10)
		self.backButtonImage = pygame.transform.scale(Const.BACK_BUTTON_IMAGE, self.backButtonSize)
		self.backButtonCoord = ((self.screenWidth - self.backButtonSize[0]) / 2, playerContainerInitCoord[1] + self.playerContainerSize[1] + (self.screenHeight - (playerContainerInitCoord[1] + self.playerContainerSize[1]) - self.backButtonSize[1]) / 2)
		self.backButton = ButtonClass.Button(self.backButtonImage, self.backButtonCoord)

	def Run(self):
		pygame.mixer.Sound.play(Const.LEADERBOARD_SOUND)
		while self.running:
			self.clock.tick(10)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			# Back Button
			self.backButton.draw(self.gameScreen)

			backState = self.backButton.isClicked(self.gameScreen)
			if backState == True:
				running = False
				menuGame = MenuClass.Menu()
				menuGame.Run()
				break

			for i in self.playerContainer:
				i.Display()

			pygame.display.update()