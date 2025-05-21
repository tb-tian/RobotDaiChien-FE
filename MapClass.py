import pygame
import Const
import CellClass
import json
import copy

def getMap(jsonFile, step):
	print(f"Step: {step}" + " Json file: " + jsonFile)
	mapFile = open(jsonFile)
	mapData = json.load(mapFile)

	curMap = []

	curList = mapData[str(step)]['map']['grid']

	m = mapData[str(step)]['map']['rows']
	n = mapData[str(step)]['map']['columns']

	for i in curList:
		row = []
		for j in i:
			row.append(j)
		curMap.append(row)

	powerUps = mapData[str(step)]['powerups']

	return (m, n, curMap, powerUps)

def getMapData(jsonFile):
	mapFile = open(jsonFile)
	mapData = json.load(mapFile)

	return mapData

class Map():
	def __init__(self, gameScreen, jsonFile, mapWidth, mapHeight, mapCoordX, mapCoordY):
		self.gameScreen = gameScreen

		# Map List
		self.jsonFile = jsonFile
		self.M, self.N, self.mapList, self.powerupList = getMap(jsonFile, 0)
		# Map Image
		self.mapWidth = mapWidth
		self.mapHeight = mapHeight
		self.mapImage = []

		self.cellLenX = self.mapWidth / self.N
		self.cellLenY = self.mapHeight / self.M
		self.cellLen = self.cellLenX
		self.mapCoordX = mapCoordX
		self.mapCoordY = mapCoordY

		pygame.draw.rect(self.gameScreen, Const.MAP_COLOR, pygame.Rect(mapCoordX, mapCoordY, mapWidth, mapHeight))

		# Create List Cell in Map
		for i in range(0, self.M):
			mapImageRow = []
			for j in range(0, self.N):
				if self.mapList[i][j] == '.':
					mapImageRow.append(CellClass.EmptyCell(self.gameScreen, (j * self.cellLenX + self.mapCoordX, i * self.cellLenX + self.mapCoordY), (i, j), self.cellLen, 0))
				elif self.mapList[i][j] == '#':
					mapImageRow.append(CellClass.ObstacleCell(self.gameScreen, (j * self.cellLenX + self.mapCoordX, i * self.cellLenX + self.mapCoordY), (i, j), self.cellLen))
			self.mapImage.append(mapImageRow)

		# Create List PowerUp Cell in Map
		self.powerUpCells = []

		for i in range(len(self.powerupList)):
			powerup_item = self.powerupList[i]
			x = int(powerup_item['x'])
			y = int(powerup_item['y'])
			type = powerup_item['type']
			if type == 'G':
				self.powerUpCells.append(CellClass.TangTocCell(self.gameScreen, (y * self.cellLenX + self.mapCoordX, x * self.cellLenX + self.mapCoordY), (x, y), self.cellLen))
			elif type == 'E':
				self.powerUpCells.append(CellClass.MauNoCell(self.gameScreen, (y * self.cellLenX + self.mapCoordX, x * self.cellLenX + self.mapCoordY), (x, y), self.cellLen))
			elif type == 'F':
				self.powerUpCells.append(CellClass.DauTronCell(self.gameScreen, (y * self.cellLenX + self.mapCoordX, x * self.cellLenX + self.mapCoordY), (x, y), self.cellLen))
		
		
		# Create Graph
		for i in range(0, self.M):
			for j in range(0, self.N):
				for dir in range(0, 4):
					ni = i + Const.CELL_MOVE[dir][0]
					nj = j + Const.CELL_MOVE[dir][1]
					if ni < 0 or ni >= self.N or nj < 0 or nj >= self.N or isinstance(self.mapImage[ni][nj], CellClass.ObstacleCell):
						continue
					self.mapImage[i][j].AddAdj(self.mapImage[ni][nj], dir)

	def DisplayMap(self):
		for mapImageRow in self.mapImage:
			for cell in mapImageRow:
				cell.DisplayBackgroundImage()

	def DisplayPowerUp(self):
		for cell in self.powerUpCells:
			cell.DisplayBackgroundImage()

	def UpdateMap(self, step, curOutsideZone):
		newMapList = getMap(self.jsonFile, step)[2]

		for i in range(self.M):
			for j in range(self.N):
				if self.mapList[i][j] == "." and newMapList[i][j] == Const.MAP_OZ:
					self.mapImage[i][j].LockCell()
				elif self.mapList[i][j] == "#":
					curRound = min(i + 1, j + 1, self.M - i, self.N - j)
					if curRound <= curOutsideZone:
						if isinstance(self.mapImage[i][j], CellClass.ObstacleCell):
							self.mapImage[i][j].LockCell()
				elif newMapList[i][j].isupper():
					newColor = 0
					if newMapList[i][j] == "A":
						newColor = 1
					elif newMapList[i][j] == "B":
						newColor = 2
					elif newMapList[i][j] == "C":
						newColor = 3
					elif newMapList[i][j] == "D":
						newColor = 4
					self.mapImage[i][j] = CellClass.EmptyCell(self.gameScreen, (j * self.cellLenX + self.mapCoordX, i * self.cellLenX + self.mapCoordY), (i, j), self.cellLen, newColor)
				elif newMapList[i][j].islower():
					newColor = 5
					if newMapList[i][j] == "a":
						newColor = 6
					elif newMapList[i][j] == "b":
						newColor = 7
					elif newMapList[i][j] == "c":
						newColor = 8
					elif newMapList[i][j] == "d":
						newColor = 9
					self.mapImage[i][j] = CellClass.EmptyCell(self.gameScreen, (j * self.cellLenX + self.mapCoordX, i * self.cellLenX + self.mapCoordY), (i, j), self.cellLen, newColor)
					# self.mapImage[i][j].LockCell()
		self.mapList = newMapList
	
	def UpdatePowerUps(self, step):
		self.powerupList = getMap(self.jsonFile, step)[3]
		self.powerUpCells.clear()

		for i in range(len(self.powerupList)):
			powerup_item = self.powerupList[i]
			x = int(powerup_item['x'])
			y = int(powerup_item['y'])
			type = powerup_item['type']
			if type == 'G':
				self.powerUpCells.append(CellClass.TangTocCell(self.gameScreen, (y * self.cellLenX + self.mapCoordX, x * self.cellLenX + self.mapCoordY), (x, y), self.cellLen))
			elif type == 'E':
				self.powerUpCells.append(CellClass.MauNoCell(self.gameScreen, (y * self.cellLenX + self.mapCoordX, x * self.cellLenX + self.mapCoordY), (x, y), self.cellLen))
			elif type == 'F':
				self.powerUpCells.append(CellClass.DauTronCell(self.gameScreen, (y * self.cellLenX + self.mapCoordX, x * self.cellLenX + self.mapCoordY), (x, y), self.cellLen))

	def GetCell(self, row, col):
		return self.mapImage[row % self.N][col % self.N]

	def getScore(self, step, ID):
		curMapData = getMapData(self.jsonFile)
		return curMapData[str(step)]["players"][str(ID)]['area']

	def getAlive(self, step, ID):
		curMapData = getMapData(self.jsonFile)
		return curMapData[str(step)]["players"][str(ID)]['alive']

	def getFrequency(self, step):
		curMapData = getMapData(self.jsonFile)
		return curMapData[str(step)]['frequency']
