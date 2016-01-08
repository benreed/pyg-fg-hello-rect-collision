"""
Boilerplate main game module to better encapsulate main loop phases
Written Dec 18, 2015 by Benjamin Reed
	
Credit for this implementation goes to Sean J. McKiernan
(Mekire) at /r/pygame
https://github.com/Mekire
"""
import sys
import Queue

import pygame as pyg
import constants as con
from game_object import *
from input import *
from stage import *

class App:
    """
    A class to cleanly encapsulate main game loop phases,
    including initialization, event handling, and state 
    updates
    """
    def __init__(self):
        """
        Get a reference to the display surface; set up required attributes;
        and instantiate player and stage objects
        """
        self.screen = pyg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pyg.time.Clock()
        self.fps = con.TARGET_FPS
		
        # Boolean members
        self.done = False
		
        # Key state variable
        self.keys = pyg.key.get_pressed()
		
        # Initialize player character(s)
        self.player = PlayerCharacter(con.PHOEBE)
		
        # Initialize stage(s)
        self.test_stage = PlayStage(self.player)
        self.stage_list = []
        self.stage_list.append(self.test_stage)
        self.stage_index = 0
        self.current_stage = self.stage_list[self.stage_index]
		
    def event_loop(self):
        """
        Method encompassing one trip through the event queue
        Called within main_loop()
        """
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.done = True
            elif event.type in (pyg.KEYUP, pyg.KEYDOWN):
                self.keys = pyg.key.get_pressed()
				
    def render(self):
        """
        Draws to the screen and updates the display
        """
		
        # Draw level
        self.current_stage.draw(self.screen)
		
        # Draw game objects
        self.player.draw(self.screen)
		
        # Update display 
        pyg.display.flip()
		
    def main_loop(self):
        """
        Performs the main game loop
        """
        while not self.done:
            self.event_loop()
            self.player.update(self.keys)
            self.render()
            self.clock.tick(self.fps)
			
def main():
    """
    Main program function. Performs Pygame initialization,
    starts, and exits the program.
    """
    pyg.init()
    pyg.display.set_caption(con.WINDOW_CAPTION)
    pyg.display.set_mode(con.SCREEN_SIZE)
    App().main_loop()
    pyg.quit()
    sys.exit()
	
if __name__ == "__main__":
    main()