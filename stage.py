"""
Module for game stages and stage-specific 
classes/functions (e.g. platforms and 
other physical stage elements)
Written Jan 5, 2016 by Benjamin Reed
Version 0.0.1-alpha
"""
import pygame as pyg
import constants as con

class GameSurface(pyg.sprite.Sprite):
    """
    Class representing a basic physical surface
    that game objects can interact with
    """
    def __init__(self, width=10, height=10):
        """
        Makes a basic Sprite with a green rect 
        Surface as a placeholder image
        """
        super(GameSurface, self).__init__()
        self.image = pyg.Surface([width, height])
        self.image.fill(con.GREEN)
        self.rect = self.image.get_rect()
    def draw(self, screen):
	    screen.blit(self.image, self.rect)

class Stage(object):
    """
    Stage superclass for basic functionality
    """
    def __init__(self):
        """
        Sets background to basic colored Surface that
        covers the whole game window
        """
        self.background = pyg.Surface(con.SCREEN_SIZE)
        self.background.fill(con.BG_COLOR)

    def draw(self, screen):
        """
        Wipe contents of previous frame and blit
        background
        """
        screen.fill(con.BLACK)
        screen.blit(self.background,(0,0))

class PlayStage(Stage):
    """
    A Stage in which gameplay occurs
    """
    def __init__(self, player):
        super(PlayStage, self).__init__()
        self.player = player
        self.surface_list = []
        level = [ [con.SCREEN_WIDTH, 15, 0, (con.SCREEN_HEIGHT-15)],
		          [con.SCREEN_WIDTH, 15, 0, 0],
				  [15, con.SCREEN_HEIGHT, 0, 0],
				  [15, con.SCREEN_HEIGHT, (con.SCREEN_WIDTH-15), 0]
		]

        for surface in level:
            wall = GameSurface(surface[0], surface[1])
            wall.rect.x = surface[2]
            wall.rect.y = surface[3]
            self.surface_list.append(wall)

    def draw(self, screen):
        super(PlayStage, self).draw(screen)
        for surface in self.surface_list:
            surface.draw(screen)