import pygame
import Const
import CellClass
import PortalClass
import PlayerStatus

class Player():
	def __init__(self, gameScreen, ID, playerName, statusInfo, curCell):
		# Status
		self.playerID = ID
		self.isAlive = True
		self.playerName = playerName
		print(playerName)
		self.status = PlayerStatus.PlayerStatus(gameScreen, ID, self.isAlive, playerName, Const.PLAYER_COLOR[ID], statusInfo[0][ID], statusInfo[1])

		self.gameScreen = gameScreen
		self.playerCell = curCell
		self.playerCell.AddPlayer(self.playerID)
		self.playerCoord = (-1, -1)
		self.playerFrameHeight = self.playerCell.GetLen() / 6 * 7
		self.playerFrameWidth = self.playerFrameHeight / 7 * 5
		# self.playerPadding = ((self.playerCell.GetLen() - self.playerFrameWidth) / 2, (self.playerCell.GetLen() - self.playerFrameHeight) * 2) 
		self.playerPadding = ((self.playerCell.GetLen() - self.playerFrameWidth) / 2 + self.playerCell.GetLen() / 15, (- self.playerFrameHeight) / 2) 

		self.playerFrame = []
		for listFrame in Const.PLAYER_FRAME_LIST:
			playerFrameList = []
			step = len(listFrame) // 4
			for i in range(self.playerID * step, self.playerID * step + step):
				frame = listFrame[i]
				playerFrameList.append(pygame.transform.scale(frame, (self.playerFrameWidth, self.playerFrameHeight)))
			self.playerFrame.append(playerFrameList)

		self.moveDirection = 2
		self.animationDirection = 0
		self.curFrame = 0
		self.numFrame = len(self.playerFrame[self.animationDirection])
		self.isMoving = False
		self.moveSpeed = 30
		self.original_move_speed = 30 # Store original speed
		self.pending_next_target = None # For multi-cell moving

		self.playerPortal = PortalClass.Portal(gameScreen, curCell)
		self.appearFrame = 9

	def GetInfo(self):
		return self.status.GetInfo()

	def UpdateCoord(self):
		if self.playerCoord == (-1, -1):
			self.playerCoord = self.playerCell.GetPlayerPos(self.playerID)

	def DisplayFrame(self):
		self.gameScreen.blit(self.playerFrame[self.animationDirection][self.curFrame], (self.playerCoord[0] + self.playerPadding[0], self.playerCoord[1] + self.playerPadding[1]))

	def GetCoord(self):
		return self.playerCell.GetCellIndex()
	
	def GetIsMoving(self):
		return self.isMoving or self.appearFrame > 0

	def GetID(self):
		return self.playerID

	def GetIsAlive(self):
		return self.isAlive

	def MoveFrame(self):
		if(self.appearFrame > 0):
			pygame.mixer.Sound.play(Const.PLAYER_APPEAR_SOUND)
			self.playerPortal.MoveFrame()
			self.appearFrame -= 1
			return
		if self.isMoving:
			self.MovePlayer()
		self.DisplayFrame()
		self.curFrame = (self.curFrame + 1) % self.numFrame

	def MovePlayer(self):
		if not self.isMoving:
			# Ensure speed is reset if movement is not active for any reason.
			# This handles cases where isMoving might be set to False externally or before a move starts.
			if self.moveSpeed != self.original_move_speed:
				self.moveSpeed = self.original_move_speed
			return

		# current_step_target_cell is the adjacent cell player is moving towards in this step.
		current_step_target_cell = self.playerCell.GetAdj(self.moveDirection) 
		
		if not current_step_target_cell:
			# Invalid move direction or blocked path that wasn't foreseen by ChangeCell.
			self.isMoving = False
			self.moveSpeed = self.original_move_speed # Reset speed on invalid move
			return

		target_coord_for_animation_step = current_step_target_cell.GetPlayerPos(self.playerID)

		# Check if player's animated coordinates have reached the center of current_step_target_cell
		if self.playerCoord == target_coord_for_animation_step:
			# Player has arrived at current_step_target_cell
			
			old_cell = self.playerCell
			self.playerCell = current_step_target_cell # Update current cell to the one just reached
			# self.playerCoord is already at target_coord_for_animation_step.

			# Manage player presence in cells
			if old_cell != self.playerCell: # Check if it's genuinely a new cell
				old_cell.RemovePlayer(self.playerID)
				self.playerCell.AddPlayer(self.playerID)

			if self.pending_next_target:
				final_target_cell_index = self.pending_next_target
				
				if self.playerCell.GetCellIndex() == final_target_cell_index:
					# Arrived at the final destination of a multi-step move
					self.isMoving = False
					self.pending_next_target = None
					self.moveSpeed = self.original_move_speed # Reset speed upon final arrival
				else:
					# Arrived at an intermediate cell (self.playerCell).
					# Need to continue to final_target_cell_index without stopping.
					# self.isMoving remains True.
					found_next_direction = False
					for direction_idx in range(4): # Check all 4 directions
						adjCell_from_intermediate = self.playerCell.GetAdj(direction_idx)
						if adjCell_from_intermediate and adjCell_from_intermediate.GetCellIndex() == final_target_cell_index:
							self.moveDirection = direction_idx # Set new direction for the next leg
							self.pending_next_target = None   # Clear pending_next_target as we are now on the final leg.
							found_next_direction = True
							 # Speed remains as set by ChangeCell (e.g., 30 for 2-step move)
							break 
					
					if not found_next_direction:
						# Fallback: if next step from intermediate to final not found.
						# This implies an issue with 2-step path logic or map change.
						self.isMoving = False
						self.pending_next_target = None # Clear, as we can't proceed.
						self.moveSpeed = self.original_move_speed # Reset speed if path breaks
			else:
				# No pending_next_target, so this was the end of a single-step move.
				self.isMoving = False
				self.moveSpeed = self.original_move_speed # Reset speed on single step completion
			
			# Whether movement stops or continues to the next leg, this step's arrival is processed.
			# Return to allow next game tick to animate the next leg if applicable, or to stop.
			return 
		
		# If not yet arrived at target_coord_for_animation_step, continue animation.
		# This is the animation code from lines 96-105 of the original snippet.
		newCoord = []
		for i in range(0, 2):
			moveLen = min(abs(target_coord_for_animation_step[i] - self.playerCoord[i]), self.moveSpeed)
			newCoord.append(self.playerCoord[i])
			if(target_coord_for_animation_step[i] > self.playerCoord[i]):
				newCoord[i] += moveLen
			elif(target_coord_for_animation_step[i] < self.playerCoord[i]):
				newCoord[i] -= moveLen
		self.playerCoord = tuple(newCoord)

	def ChangeAnimation(self, newAnimation):
		if self.animationDirection != newAnimation:
			self.animationDirection = newAnimation
			self.curFrame = 0
			self.numFrame = len(self.playerFrame[self.animationDirection])

	def ChangeDirection(self, newDirection):
		if self.isMoving or newDirection > 3 or newDirection < 0:
			return
		if self.moveDirection != newDirection:
			self.moveDirection = newDirection
		if newDirection == 1 or newDirection == 3:
			self.ChangeAnimation(newDirection // 2)

		if self.playerCell.GetAdj(self.moveDirection) != None and self.isMoving == False:
			self.playerCell.RemovePlayer(self.playerID)
			self.playerCell.GetAdj(self.moveDirection).AddPlayer(self.playerID)
			self.isMoving = True

	def ChangeCell(self, newCellIndex):
		if self.isMoving:
			return
		
		current_cell_index = self.GetCoord()
		target_x, target_y = newCellIndex
		current_x, current_y = current_cell_index

		if current_cell_index == newCellIndex:
			self.pending_next_target = None # Reached target or target is current location
			self.moveSpeed = self.original_move_speed # Ensure original speed if not moving
			return
		
		# Try direct 1-step move first
		for direction in range(4):
				adjCell = self.playerCell.GetAdj(direction)
				if adjCell and adjCell.GetCellIndex() == newCellIndex:
					self.pending_next_target = None # Clear any pending multi-step target if making a direct move
					self.moveSpeed = self.original_move_speed # Set original speed for 1-step move
					self.ChangeDirection(direction)
					return
		
		# Try 2-step move
		if current_x != -1 and current_y != -1:
			intermediate_cell_index = None
			# Check for horizontal 2-cell jump
			if current_y == target_y and abs(current_x - target_x) == 2:
				mid_x = (current_x + target_x) // 2
				intermediate_cell_index = (mid_x, current_y)
			# Check for vertical 2-cell jump
			elif current_x == target_x and abs(current_y - target_y) == 2:
				mid_y = (current_y + target_y) // 2
				intermediate_cell_index = (current_x, mid_y)
			
			if intermediate_cell_index:
				for direction_to_intermediate in range(4):
					adjCell = self.playerCell.GetAdj(direction_to_intermediate)
					if adjCell and adjCell.GetCellIndex() == intermediate_cell_index:
						# Check if the intermediate cell itself is not an obstacle before proceeding
						if isinstance(adjCell, CellClass.ObstacleCell):
							continue # Cannot use this intermediate cell

						# Check if the final target cell (newCellIndex) is reachable from intermediate_cell_index
						# This requires looking one step ahead from the intermediate cell
						can_reach_final_from_intermediate = False
						for final_direction_check in range(4):
							final_adj_cell = adjCell.GetAdj(final_direction_check)
							if final_adj_cell and final_adj_cell.GetCellIndex() == newCellIndex and not isinstance(final_adj_cell, CellClass.ObstacleCell):
								can_reach_final_from_intermediate = True
								break
						
						if can_reach_final_from_intermediate:
							self.pending_next_target = newCellIndex # Set the original target as pending
							self.moveSpeed = 60 # Set special speed for 2-step move
							self.ChangeDirection(direction_to_intermediate) # Start moving to the intermediate cell
							return
		
		# If no path found (direct or 2-step), ensure speed is original.
		self.moveSpeed = self.original_move_speed

	def HandleEvent(self):
		key = pygame.key.get_pressed()

		if key[pygame.K_UP]:
			self.ChangeDirection(0)
		if key[pygame.K_DOWN]:
			self.ChangeDirection(2)
		if key[pygame.K_LEFT]:
			self.ChangeDirection(3)
		if key[pygame.K_RIGHT]:
			self.ChangeDirection(1)

	def drawStatus(self):
		self.status.displayStatusImage()

	def updateScore(self, curScore):
		self.status.updateScore(curScore)

	def updateAlive(self, isAlive):
		if self.isAlive == True and isAlive == False:
			pygame.mixer.Sound.play(Const.PLAYER_DIE_SOUND)
			self.ChangeAnimation(2)
		self.isAlive = isAlive
		self.status.updateAlive(isAlive)