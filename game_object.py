"""
Module for game objects as managed by 
game stages
Written Jan 5, 2016 by Benjamin Reed
Version 0.0.1-alpha
"""
import pygame as pyg
import constants as con
from animation import *

class MovableObject(object):
	"""
	Basic game object that can be 
	moved on screen (has a deltaX and deltaY)
	"""
	def __init__(self):
		self.deltaX = 0
		self.deltaY = 0
		
class PlayerCharacter(MovableObject):
	"""
	Game object representing a player-controllable
	character
	"""
	def __init__(self, chara):
		"""
		Instantiates a character based on attributes
		passed in from the constants module
		"""
		super(PlayerCharacter, self).__init__()
		self.direction = "R"
		
		# This is a dict rather than a list because:
		#   (1) I want to refer to frames by name (key)
		#   (2) IIRC lookup time scales better for large
		#       numbers of elements in dicts than lists
		#       (may eventually be looking at 100+ frames
		#       for a single character
		#   (3) Strict ordering shouldn't be necessary
		#       after initialization; so long as I can 
		#       look up a frame by key, I should be 
		#       able to re-establish any logical ordering
		#       based on the key (run1, run2, run3, etc)
		self.anim_frames_R = {}
		
		self.load_frames(chara)
		self.current_frame = self.anim_frames_R["IDLE_1"]
		
		# Reference to current Stage character is
		#   associated with/inhabiting
		self.stage = None
	
	def draw(self, screen):
		"""
		Draws character image to display
		"""
		pyg.draw.rect(self.current_frame.image, con.GREEN, self.current_frame.sprite_rect, 1)
		for vuln in self.current_frame.vuln_rects:
			pyg.draw.rect(self.current_frame.image, con.CYAN, vuln, 1)
		screen.blit(self.current_frame.image, self.current_frame.rect)
		
	def load_frames(self, chara):
		"""
		Loads animation frames and their associated collision
		rects for that character
		"""
		sprite_sheet = SpriteSheet(chara["SPRITESHEET"])
		originX = originY = 0
		image_width = chara["IMAGE_WIDTH"]
		image_height = chara["IMAGE_HEIGHT"]
		
		for x in range (0, chara["NUM_OF_FRAMES"]):
			# Slice image
			image = sprite_sheet.get_image(originX, originY, image_width, image_height)
			name = str(chara["ANIMS"][x][0])
			rects = []
			
			# Make typed rects from character constants
			for y in range(1, len(chara["ANIMS"][x])):
				#print str(chara["ANIMS"][x][y])
				#rect = RectWithType(chara["ANIMS"][x][y])
				#print "Rect is now: " + str(rect)
				#rects.append(rect)
				rects.append(RectWithType(chara["ANIMS"][x][y]))
				
			# Combine rects and image to make an AnimationFrame
			frame = AnimationFrame(name, image, rects)
			
			# Append frame to dict of animation frames 
			#   with name flag as key
			self.anim_frames_R[chara["ANIMS"][x][0]] = frame