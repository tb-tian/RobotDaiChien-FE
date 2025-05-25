import pygame
import json
import os

pygame.mixer.init()

MSI = (1536, 864)
DELL = (1280, 720)

NUM_MAP = len([f for f in os.listdir('Assets/Map') if os.path.isfile(os.path.join('Assets/Map', f))])

# Player
PLAYER_COLOR = ["RED", "GREEN", "BLUE", "YELLOW"]
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (146, 146, 146)
WHITE = (255, 255, 255)
SNOW = (255, 250, 250)
BLACK = (0, 0, 0)
PLAYER_COLOR_DICT = {
	"RED": (255, 0, 0),
	"GREEN": (0, 255, 0),
	"BLUE": (0, 0, 255),
	"YELLOW": (255, 255, 0)
}
MAP_COLOR = (127, 115, 82)
BACKGROUND_COLOR = (92, 98, 108)

GAME_BACKGROUND = pygame.image.load('Assets/Images/Background/Game-Background.png')

PLAYER_AVA = [pygame.image.load(f'Assets/Images/Status/Avatar_{i}.png') for i in range(1, 5)]
PLAYER_AVA_DEAD = [pygame.image.load(f'Assets/Images/Status/deadAvatar_{i}.png') for i in range(1, 5)]

CELL_LENGTH = 100
CELL_IMAGE_LIST = [pygame.image.load(f'Assets/Images/Cell/tile_{i}.png') for i in range(12)]
CELL_MOVE = [(-1, 0), (0, 1), (1, 0), (0, -1)]
PLAYER_FRAME_LIST = [
	[pygame.image.load(f'Assets/Images/Player/player{i}-left-{j}.png') for i in range(1, 5) for j in range(1, 5)],
	[pygame.image.load(f'Assets/Images/Player/player{i}-right-{j}.png') for i in range(1, 5) for j in range(1, 5)],
	[pygame.image.load(f'Assets/Images/Player/player{i}-die-{j}.png') for i in range(1, 5) for j in range(1,2)]
]
PORTAL_FRAME_LIST = [pygame.image.load(f'Assets/Images/Portal/portal-{i}.png') for i in range(9)]

# PowerUps
TANG_TOC = pygame.image.load(f'Assets/Images/PowerUps/tangtoc.png')
DAU_TRON = pygame.image.load(f'Assets/Images/PowerUps/dautron.png')
MAU_NO = pygame.image.load(f'Assets/Images/PowerUps/mauno.png')

# Map file
MAP_NORM = '.'
MAP_OBS = '#'
MAP_OZ = '*'

# Leaderboard
LEADERBOARD_BG = pygame.image.load("Assets/Images/Background/Leaderboard-Background.png")
RANK_CUP = [
	pygame.image.load(f'Assets/Images/Leaderboard/rank{i}.png') for i in range(1, 5)
]
BACK_BUTTON_IMAGE = pygame.image.load('Assets/Images/Leaderboard/back-button.png')

# Menu
MENU_BACKGROUND = pygame.image.load('Assets/Images/Background/Menu-Background.png')
NHA_TAI_TRO = pygame.image.load('Assets/Images/Background/NhaTaiTro.png')
START_BUTTON_IMAGE = pygame.image.load('Assets/Images/Menu/start-button.png')
TWO_PLAYER_IMAGE = pygame.image.load('Assets/Images/Menu/2player-button.png')
FOUR_PLAYER_IMAGE = pygame.image.load('Assets/Images/Menu/4player-button.png')
CHOOSE_IMAGE = pygame.image.load('Assets/Images/Menu/choose.png')
TICK_IMAGE = [
	pygame.image.load('Assets/Images/Menu/checkbox-unchecked.png'),
	pygame.image.load('Assets/Images/Menu/checkbox-checked.png')
]
MAP_SIZE_IMAGE = pygame.image.load('Assets/Images/Menu/dropdown.png')
UP_BUTTON_IMAGE = pygame.image.load('Assets/Images/Menu/up.png')
DOWN_BUTTON_IMAGE = pygame.image.load('Assets/Images/Menu/down.png')

# Sound
CLICK_BUTTON_SOUND = pygame.mixer.Sound("Assets/Sounds/click_button.mp3")
PLAYER_APPEAR_SOUND = pygame.mixer.Sound("Assets/Sounds/player_appear.mp3")
PLAYER_DIE_SOUND = pygame.mixer.Sound("Assets/Sounds/player_die.mp3")
LEADERBOARD_SOUND = pygame.mixer.Sound("Assets/Sounds/leaderboard.mp3")
INGAME_SOUND = pygame.mixer.Sound("Assets/Sounds/ingame_1.mp3")

# Player Name List
PLAYER_NAME_LIST = ['NHMinh', 'NCChuong', 'HDVu', 'NHMTam']
