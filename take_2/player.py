"""
Module defining player character functionality
Written Jan 11, 2016 by Benjamin Reed
Version 0.0.1-alpha
"""

import pygame as pyg
import constants as con
from game_object import *

class PlayerCharacter(MovableObject):
    def __init__(self, chara):
        super(PlayerCharacter, self).__init__()
        
        # Collision rect members
        self.control_rect = pyg.Rect(self.x, self.y, 30, 50)
        #self.rects.append(pyg.Rect(self.x, self.y, 30, 50))
        self.rects.append(self.control_rect)
        self.rects.append(pyg.Rect(self.x+5, self.y+5, 20, 20))
        self.rects.append(pyg.Rect(self.x+10, self.y+10, 20, 20))
        self.gravity = chara["GRAVITY"]
        self.keys = None
        
    def update(self, keys):
        # Apply gravity
        self.apply_grav()
    
        # Update key state and handle input
        self.keys = keys
        
        # Apply deltaX
        #for rect in self.rects:
            #rect.x += self.deltaX
        self.moveX()
        
        # Collision behavior (x-axis)
        
        # Apply deltaY
        #for rect in self.rects:
            #rect.y += self.deltaY
        self.moveY()    
        # Collision behavior (y-axis)
        
    def draw(self, screen):
        if con.DEBUG:
            for rect in self.rects:
                pyg.draw.rect(screen, con.WHITE, rect, 1)
            
    """
    Methods called by update(), draw(), or __init__()
    """
    