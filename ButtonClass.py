import pygame
import Const

class Button() :
	def __init__(self, image, initCoord):
		width = image.get_width()
		height = image.get_height() 
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (initCoord[0], initCoord[1])
		self.clicked = False

	def draw(self, gameScreen):
		gameScreen.blit(self.image , (self.rect.x , self.rect.y))

	def isClicked(self, gameScreen): 
		action = False 

		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos) :
			if(pygame.mouse.get_pressed()[0] == 1  and self.clicked == False):
				pygame.mixer.Sound.play(Const.CLICK_BUTTON_SOUND)
				self.clicked = True
				action = True 
		if(pygame.mouse.get_pressed()[0] == 0): 
			self.clicked = False 
		return action 