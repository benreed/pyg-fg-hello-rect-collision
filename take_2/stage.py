"""
Module for game "stages", including both
stages where gameplay takes place and 
configuration screens
Also includes basic stage objects such as 
surfaces
Written Jan 11, 2016 by Benjamin Reed
Version 0.0.1-alpha

Credit for original implementation goes to
Paul Vincent Craven at 
programarcadegames.com
"""

import pygame as pyg
import constants as con

"""
Stage constants defined up here
"""
# Simplifying concept for now -- working only with a box
#   made of lines to delineate stage boundaries
TESTSTAGE = {
    "FLOOR"      : con.SCREEN_HEIGHT-15,
    "CEILING"    : 15,
    "LEFT_WALL"  : 15,
    "RIGHT_WALL" : con.SCREEN_WIDTH-15
}

class Stage(object):
    """
    Generic stage superclass. Has basic functionality
    to wipe and update display contents.
    """
    def __init__(self):
        """
        Initializes background to a window-sized surface
        colored with the background color
        """
        self.background = pyg.Surface([con.SCREEN_WIDTH, con.SCREEN_HEIGHT])
        self.background.fill(con.BG_COLOR)
        
    def draw(self, screen):
        """
        Blits the background color to display surface
        to wipe previous frame's contents
        """
        screen.blit(self.background,[0,0])
        
class PlayStage(Stage):
    """
    A Stage meant to manage gameplay objects, including 
    player characters, background objects, etc.
    """
    def __init__(self, stage, player):
        """
        Calls superconstructor 
        Also adds a reference to any pre-declared 
        Player objects it is expected to know & manage
        """
        super(PlayStage, self).__init__()
        self.player = player
        self.floor = stage["FLOOR"]
        self.ceiling = stage["CEILING"]
        self.left_wall = stage["LEFT_WALL"]
        self.right_wall = stage["RIGHT_WALL"]
            
    def draw(self, screen):
        """
        Wipes previous frame's contents with 
        background and draws game surface members
        """
        # Blit background 
        screen.blit(self.background,[0,0])
        
        # Draw primitive lines to delineate ceiling,
        #   floor, and walls
        pyg.draw.line(screen, con.GREEN, (0, self.floor), (con.SCREEN_WIDTH, self.floor))
        pyg.draw.line(screen, con.GREEN, (0, self.ceiling), (con.SCREEN_WIDTH, self.ceiling))
        pyg.draw.line(screen, con.GREEN, (self.left_wall, 0), (self.left_wall, con.SCREEN_HEIGHT))
        pyg.draw.line(screen, con.GREEN, (self.right_wall, 0), (self.right_wall, con.SCREEN_HEIGHT))