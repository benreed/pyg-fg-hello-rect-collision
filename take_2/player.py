"""
Module defining player character functionality
Written Jan 11, 2016 by Benjamin Reed
Version 0.0.1-alpha
"""

import pygame as pyg
import constants as con
from game_object import *
from spritesheet import *

class PlayerCharacter(MovableObject):
    def __init__(self, chara):
        super(PlayerCharacter, self).__init__()

        # Initialize animation frames
        self.anim_frames_R = {}
        self.anim_frames_L = {}
        self.init_frames(chara)
        self.current_frame = self.anim_frames_R["IDLE_1"]
        img_rect = self.current_frame.get_rect()
        self.draw_rect = TypedRect("Sprite", img_rect.x, img_rect.y, img_rect.width, img_rect.height)
        self.draw_rect.x = self.x
        self.draw_rect.y = self.y
        
        # Collision rect members
        self.rects.append(TypedRect("Vuln", self.x+5, self.y+5, 20, 20))
        self.rects.append(self.draw_rect)

        # Physics/numeric members
        self.gravity = chara["GRAVITY"]

        # Logical state members    
        self.keys = None
        self.landed = False

        # Reference to stage character inhabits (set externally)
        self.stage = None
        
    def update(self, keys):
        # Apply gravity
        self.apply_grav()
    
        # Update key state and handle input
        self.keys = keys
        
        # Apply deltaX
        self.moveX()
        
        # Collision behavior (x-axis)
        
        # Apply deltaY
        self.moveY()
    
        # Collision behavior (y-axis)
        # (1. Check control rect bottom against floor)
        if self.control_rect.bottom >= self.stage.floor:
            self.land(self.stage.floor)
        
    def draw(self, screen):
        screen.blit(self.current_frame, self.draw_rect)
        if con.DEBUG:
            pyg.draw.rect(screen, con.WHITE, self.draw_rect, 1)
            for rect in self.rects:
                if rect.type == "Vuln":
                    pyg.draw.rect(screen, con.BLUE, rect, 1)
                else:
                    pyg.draw.rect(screen, con.WHITE, rect, 1)
            
    """
    Methods called by update(), draw(), or __init__()
    """
    
    def init_frames(self, chara):
        sprite_sheet = SpriteSheet(chara["SPRITESHEET"])
        originX = originY = 0
        img_width = chara["IMAGE_WIDTH"]
        img_height = chara["IMAGE_HEIGHT"]
        
        for x in range (0, chara["NUM_OF_FRAMES"]):
            image = sprite_sheet.get_image(originX, originY, img_width, img_height)
            name = chara["ANIMS"][x][0]
            print name
            self.anim_frames_R[name] = image
            originX += img_width
