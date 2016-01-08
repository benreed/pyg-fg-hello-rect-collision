"""
Module for game objects as managed by 
game stages
Written Jan 5, 2016 by Benjamin Reed
Version 0.0.1-alpha
"""
import Queue

import pygame as pyg
import constants as con
from animation import *
from input import *

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
		
        self.anim_frames_R = {}
        self.anim_frames_L = {}
        self.load_frames(chara)
        self.current_frame = self.anim_frames_R["IDLE_1"]
		
        # Movement attributes
        self.run_speed = chara["RUN_SPEED"]
        self.air_steer_speed = chara["AIR_STEER_SPEED"]
        self.movement_speed = self.run_speed
        self.jump_force = chara["JUMP_FORCE"]
        self.gravity_force = chara["GRAVITY_FORCE"]
		
        # State variables
        self.keys = None
        self.direction = "R"
        self.airborne = True
        self.air_jumped = False
        self.jumped_from_run = False
		
        # Input event queue
        self.input_queue = Queue.Queue()
		
        # Reference to current Stage character is
        #   associated with/inhabiting
        self.stage = None
		
    def update(self, keys):
        # Calculate gravity
        # self.apply_grav()
		
        # Update keystate and handle input
        self.keys = keys
		
        # Apply deltaX
        self.current_frame.rect.x += self.deltaX
		
        # Check for collisions along x-axis
		
        # Apply deltaY
        self.current_frame.rect.y += self.deltaY
		
    def draw(self, screen):
        """
        Draws character image to display
        """
        # If game is in debug mode, draw rects/drawing axis 
        #   as graphical primitives on top of frame image
        if con.DEBUG:
            pyg.draw.rect(screen, con.WHITE, self.current_frame.rect, 1)
            pyg.draw.rect(self.current_frame.image, con.GREEN, self.current_frame.sprite_rect, 1)
            if self.current_frame.vuln_rects:
                for vuln in self.current_frame.vuln_rects:
                    pyg.draw.rect(self.current_frame.image, con.CYAN, vuln, 1)
            if self.current_frame.atk_rects:
                for atk in self.current_frame.atk_rects:
                    pyg.draw.rect(self.current_frame.image, con.RED, vuln, 1)
            pyg.draw.line(self.current_frame.image, con.WHITE, (self.current_frame.axis, 0), (self.current_frame.axis, self.current_frame.image.get_height()))
			
        # Blit current frame image to screen
        screen.blit(self.current_frame.image, self.current_frame.rect)
		
    """
    Methods called by update() and/or draw()
    """
    def apply_grav(self):
        """
        Applies character-specific gravity to the character's
        deltaY
        (may later be changed to be a modifier to 
        gravity provided by the PlayStage the character
        inhabits)
        """
        if self.deltaY == 0:
            self.deltaY = 1
        else:
            self.deltaY += self.gravity_force
			
    def set_frame(self, key):
        if self.direction == "R":
            self.current_frame = anim_frames_R[key]
        else:
            self.current_frame = anim_frames_L[key]
			
    """
    Initialization methods
    """
	
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
			
            # Set frame's name and drawing axis from character constants
            name = chara["ANIMS"][x][0]
            axis = chara["ANIMS"][x][1]
			
            # Make typed rects from character constants
            rects = []
            for y in range(2, len(chara["ANIMS"][x])):
                rects.append(RectWithType(chara["ANIMS"][x][y]))
				
            # Combine rects and image to make an AnimationFrame
            #   and insert it into a dict keyed by name
            frame = AnimationFrame(name, axis, image, rects)
            self.anim_frames_R[name] = frame
			
            # Flip axis (easy transform because it's one-dimensional)
            left_axis = image_width - axis
			
            # Flip animation image horizontally
            image = pyg.transform.flip(image, True, False)
			
            # Make new rects out of old rect members, flip their 
            #   in-frame coordinates horizontally, and append them
            #   to a list
            left_rects = []
            for rect in rects:
                new_rect = RectWithType((rect.type, rect.x, rect.y, rect.width, rect.height))
                new_rect.flip_horizontal(image_width)
                left_rects.append(new_rect)
				
            # Make a new AnimationFrame out of the flipped attributes
            #   and append it to the dict of left-facing frames
            left_frame = AnimationFrame(name, left_axis, image, left_rects)
            self.anim_frames_L[name] = left_frame
			
            # Advance originX to slice next frame
            originX += image_width