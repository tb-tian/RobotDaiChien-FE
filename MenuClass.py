import pygame
import Const
import ButtonClass
import InGame

import os

def isExistInList(S, curList):
	for i in curList:
		if i == S:
			return True

	return False

def findJsonFile(listTeam, mapID):
	jsonPath = 'Assets/Json/'
	dirList = os.listdir(jsonPath)

	print(listTeam)

	n = len(listTeam)

	mapFirstChar = chr(ord('A')+ mapID - 1)

	if n == 2:
		for i in range(2):
			for j in range(2):
				curStr = mapFirstChar + '_' + Const.PLAYER_NAME_LIST[listTeam[i]] + '_' + Const.PLAYER_NAME_LIST[listTeam[j]] + '.json'

				# print("Str: " + curStr)
				if(isExistInList(curStr, dirList)):
					newListTeam = [Const.PLAYER_NAME_LIST[listTeam[i]], Const.PLAYER_NAME_LIST[listTeam[j]]]
					return (jsonPath + curStr, newListTeam)

	if n == 4:
		for i in range(4):
			for j in range(4):
				for k in range(4):
					for t in range(4):
						curStr = mapFirstChar + '_' + Const.PLAYER_NAME_LIST[listTeam[i]] + '_' + Const.PLAYER_NAME_LIST[listTeam[j]] + '_' + Const.PLAYER_NAME_LIST[listTeam[k]] + '_' + Const.PLAYER_NAME_LIST[listTeam[t]] + '.json'

						if(isExistInList(curStr, dirList)):
							newListTeam = [Const.PLAYER_NAME_LIST[listTeam[i]], Const.PLAYER_NAME_LIST[listTeam[j]], Const.PLAYER_NAME_LIST[listTeam[k]], Const.PLAYER_NAME_LIST[listTeam[t]]]
							return (jsonPath + curStr, newListTeam)
	return (-1, 0)

class Menu():
	def __init__(self):
		pygame.init()

		# Menu Screen
		if os.name == 'nt': 
			self.gameScreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		else:
			self.gameScreen = pygame.display.set_mode((1920, 1080))
		self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
		pygame.display.flip()
		pygame.display.set_caption("Robot Dai Chien")

		# Menu Background
		self.backgroundImage = pygame.transform.scale(Const.MENU_BACKGROUND, (self.screenWidth, self.screenHeight))

		print(self.screenWidth, self.screenHeight)

		##### Prepare Data For Ingame
		self.mode = 0
		self.tickMode = [0, 0, 0, 0]
		self.mapID = 1

		# Run
		self.running = True
		self.clock = pygame.time.Clock()

		# Load Start Image
		self.startButtonSize = (self.screenWidth * 1.5 / 10, self.screenHeight * 1.5 / 10)
		self.startButtonImage = pygame.transform.scale(Const.START_BUTTON_IMAGE, self.startButtonSize)
		self.startButtonCoord = (self.screenWidth / 2 + (self.screenWidth / 2 - self.startButtonSize[0]) / 2, self.screenHeight * 3 / 4 + (self.screenHeight * 1 / 4 - self.startButtonSize[1]) / 2)
		self.startButton = ButtonClass.Button(self.startButtonImage, self.startButtonCoord)

		# Mode Text
		self.modeTextFont = pygame.font.Font('Assets/Fonts/AmaticSC-Bold.ttf', 75 * self.screenWidth // Const.DELL[0])
		self.modeText = self.modeTextFont.render("MODE", True, Const.WHITE)
		modeHeight = self.modeTextFont.size("MODE")[1]
		modeWidth = self.modeTextFont.size('MODE')[0]
		self.modeTextCoord = (self.screenWidth / 2 + (self.screenWidth / 2 - modeWidth) / 2, self.screenHeight * 1 / 10)

		# Two Player Image
		self.twoPlayerSize = (self.screenWidth * 1.5 / 10, self.screenHeight * 1 / 10)
		self.twoPlayerImage = pygame.transform.scale(Const.TWO_PLAYER_IMAGE, self.twoPlayerSize)
		self.twoPlayerCoord = (self.screenWidth / 2 + (self.screenWidth / 4 - self.twoPlayerSize[0]) / 2, self.modeTextCoord[1] + modeHeight + self.screenHeight * 1 / 30)
		self.twoPlayerButton = ButtonClass.Button(self.twoPlayerImage, self.twoPlayerCoord)

		# Four Player Image
		self.fourPlayerSize = (self.screenWidth * 1.5 / 10, self.screenHeight * 1 / 10)
		self.fourPlayerImage = pygame.transform.scale(Const.FOUR_PLAYER_IMAGE, self.fourPlayerSize)
		self.fourPlayerCoord = (self.screenWidth * 3 / 4 + (self.screenWidth / 4 - self.fourPlayerSize[0]) / 2, self.modeTextCoord[1] + modeHeight + self.screenHeight * 1 / 30)
		self.fourPlayerButton = ButtonClass.Button(self.fourPlayerImage, self.fourPlayerCoord)

		# Choose Icon
		self.chooseSize = (self.twoPlayerSize[1] / 2, self.twoPlayerSize[1] / 2)
		self.chooseImage = pygame.transform.scale(Const.CHOOSE_IMAGE, self.chooseSize)
		self.chooseCoord = [
			(self.twoPlayerCoord[0] - self.chooseSize[0] - self.screenWidth * 1 / 200, self.twoPlayerCoord[1] + (self.twoPlayerSize[1] - self.chooseSize[1]) / 2),
			(self.fourPlayerCoord[0] - self.chooseSize[0] -self.screenWidth * 1 / 200, self.fourPlayerCoord[1] + (self.fourPlayerSize[1] - self.chooseSize[1]) / 2)
		]

		# Choose Team
		self.tickSize = (self.chooseSize[1] * 99 / 100, self.chooseSize[1] * 99 / 100)
		self.tickImage = [pygame.transform.scale(Const.TICK_IMAGE[i], self.tickSize) for i in range(2)]
		self.tickCoord = [
			(self.twoPlayerCoord[0] + self.tickSize[0] * 1 / 5, self.twoPlayerCoord[1] + self.twoPlayerSize[1] + self.screenHeight * 1 / 50),
			(self.fourPlayerCoord[0] + self.tickSize[0] * 1 / 5, self.fourPlayerCoord[1] + self.fourPlayerSize[1] + self.screenHeight * 1 / 50),
			(self.twoPlayerCoord[0] + self.tickSize[0] * 1 / 5, self.twoPlayerCoord[1] + self.twoPlayerSize[1] + self.tickSize[0] + self.screenHeight * 1 / 50 + self.screenHeight * 1 / 100),
			(self.fourPlayerCoord[0] + self.tickSize[0] * 1 / 5, self.fourPlayerCoord[1] + self.fourPlayerSize[1] + self.tickSize[0] + self.screenHeight * 1 / 50 + self.screenHeight * 1 / 100)
		]
		self.tickButton = [[ButtonClass.Button(self.tickImage[j], self.tickCoord[i]) for j in range(2)] for i in range(4)]

		# Team Text
		self.teamTextFont = pygame.font.Font('Assets/Fonts/VCR_OSD_MONO.ttf', 24 * self.screenWidth // Const.DELL[0])
		self.teamText = [self.teamTextFont.render(Const.PLAYER_NAME_LIST[i], True, Const.WHITE) for i in range(4)]
		teamHeight = [self.teamTextFont.size(Const.PLAYER_NAME_LIST[i])[1] for i in range(4)]
		teamWidth = [self.teamTextFont.size(Const.PLAYER_NAME_LIST[i])[0] for i in range(4)]
		self.teamCoord = [(self.tickCoord[i][0] + self.screenWidth * 1 / 200 + self.tickSize[0], self.tickCoord[i][1] + (self.tickSize[1] - teamHeight[i]) / 2) for i in range(4)]

		# Map Text
		self.mapTextFont = pygame.font.Font('Assets/Fonts/AmaticSC-Bold.ttf', 75 * self.screenWidth // Const.DELL[0])
		self.mapText = self.mapTextFont.render("MAP", True, Const.WHITE)
		mapHeight = self.mapTextFont.size("MAP")[1]
		mapWidth = self.mapTextFont.size('MAP')[0]
		self.mapTextCoord = (self.screenWidth / 2 + (self.screenWidth / 2 - mapWidth) / 2, self.screenHeight / 2)

		# Map Size Image
		self.mapSizeSize = (self.screenWidth * 5 / 20, self.screenHeight * 1 / 10)
		self.mapSizeImage = pygame.transform.scale(Const.MAP_SIZE_IMAGE, self.mapSizeSize)
		self.mapSizeCoord = (self.screenWidth / 2 + (self.screenWidth / 2 - self.mapSizeSize[0]) / 2, self.mapTextCoord[1] + mapHeight)

		# Up Button
		self.upButtonSize = (self.mapSizeSize[0] * 0.75 / 10, self.mapSizeSize[1] * 2.5 / 10)
		self.upButtonImage = pygame.transform.scale(Const.UP_BUTTON_IMAGE, self.upButtonSize)
		self.upButtonCoord = (self.mapSizeCoord[0] + self.mapSizeSize[0] - self.upButtonSize[0] - self.mapSizeSize[0] * 1 / 20, self.mapSizeCoord[1] + (self.mapSizeSize[1] / 2 - self.upButtonSize[1]) / 2)
		self.upButton = ButtonClass.Button(self.upButtonImage, self.upButtonCoord)

		# Down Button
		self.downButtonSize = (self.mapSizeSize[0] * 0.75 / 10, self.mapSizeSize[1] * 2.5 / 10)
		self.downButtonImage = pygame.transform.scale(Const.DOWN_BUTTON_IMAGE, self.downButtonSize)
		self.downButtonCoord = (self.mapSizeCoord[0] + self.mapSizeSize[0] - self.downButtonSize[0] - self.mapSizeSize[0] * 1 / 20, self.mapSizeCoord[1] + self.mapSizeSize[1] / 2 + (self.mapSizeSize[1] / 2 - self.downButtonSize[1]) / 2)
		self.downButton = ButtonClass.Button(self.downButtonImage, self.downButtonCoord)

		# Map Num Cell Text
		self.mapNumCellFont = pygame.font.Font('Assets/Fonts/AmaticSC-Bold.ttf', 40 * self.screenWidth // Const.DELL[0])
		mapNumCellStr = "MAP " + str(self.mapID)
		self.mapNumCellText = self.mapNumCellFont.render(mapNumCellStr, True, Const.WHITE)
		mapNumCellHeight = self.mapNumCellFont.size(mapNumCellStr)[1]
		mapNumCellWidth = self.mapNumCellFont.size(mapNumCellStr)[0]
		self.mapNumCellCoord = (self.mapSizeCoord[0] + (self.mapSizeSize[0] - mapNumCellWidth - self.upButtonSize[0]) / 2, self.mapSizeCoord[1] + (self.mapSizeSize[1] - mapNumCellHeight) / 2)


	def Run(self):
		while self.running:
			self.clock.tick(10)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_presses = pygame.mouse.get_pressed()

			# Mouse Process
			twoPlayerState = self.twoPlayerButton.isClicked(self.gameScreen)
			if twoPlayerState == True:
				self.mode = 0
			fourPlayerState = self.fourPlayerButton.isClicked(self.gameScreen)
			if fourPlayerState == True:
				self.mode = 1

			for i in range(4):
				tickState = self.tickButton[i][0].isClicked(self.gameScreen)
				if tickState == True:
					self.tickMode[i] = (1 - self.tickMode[i])

			startState = self.startButton.isClicked(self.gameScreen)
			if startState == True:
				listTeam = []
				for i in range(4):
					if self.tickMode[i] == 1:
						listTeam.append(i)

				jsonFile = findJsonFile(listTeam, self.mapID)[0]

				# print(jsonFile)
				if jsonFile != -1:
					newListTeam = findJsonFile(listTeam, self.mapID)[1]
					self.running = False
					InGame.Run(jsonFile, newListTeam)
					break

			upState = self.upButton.isClicked(self.gameScreen)
			if upState == True:
				self.mapID += 1
				if(self.mapID > Const.NUM_MAP): 
					self.mapID = 1
				mapNumCellStr = "MAP " + str(self.mapID)
				self.mapNumCellText = self.mapNumCellFont.render(mapNumCellStr, True, Const.WHITE)

			downState = self.downButton.isClicked(self.gameScreen)
			if downState == True:
				self.mapID -= 1
				if(self.mapID == 0): 
					self.mapID = Const.NUM_MAP
				mapNumCellStr = "MAP " + str(self.mapID)
				self.mapNumCellText = self.mapNumCellFont.render(mapNumCellStr, True, Const.WHITE)
			
			# Draw Window
			self.gameScreen.blit(self.backgroundImage, (0, 0))

			self.startButton.draw(self.gameScreen)
			self.twoPlayerButton.draw(self.gameScreen)
			self.fourPlayerButton.draw(self.gameScreen)
			self.gameScreen.blit(self.modeText, self.modeTextCoord)
			self.gameScreen.blit(self.mapText, self.mapTextCoord)
			self.gameScreen.blit(self.chooseImage, self.chooseCoord[self.mode])
			self.gameScreen.blit(self.mapSizeImage, self.mapSizeCoord)
			self.upButton.draw(self.gameScreen)
			self.downButton.draw(self.gameScreen)
			self.gameScreen.blit(self.mapNumCellText, self.mapNumCellCoord)


			for i in range(4):
				self.tickButton[i][self.tickMode[i]].draw(self.gameScreen)
				self.gameScreen.blit(self.teamText[i], self.teamCoord[i])

			pygame.display.update()

