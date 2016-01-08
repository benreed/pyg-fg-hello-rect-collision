"""
Animation module, including spritesheet 
and animation frame classes
Written Dec 29, 2015 by Benjamin Reed

Credit for original spritesheet implementation 
goes to Paul Vincent Craven at
programarcadegames.com
"""

import pygame as pyg
import constants as con

class RectWithType(pyg.Rect):
    """
    Class representing a collision rect with 
    a type flag defining what kind of collision 
    it is used for. 

    Type flag legend:

    'Sprite' : Sprite/surface collision
    'Vuln'   : Attack vulnerability region ("hurtbox")
    'Atk'    : Attack collision region ("hitbox")
    """
    def __init__(self, rect):
        super(RectWithType, self).__init__(rect[1], rect[2], rect[3], rect[4])
        self.type = rect[0]

    def flip_horizontal(self, frame_width):
        """
        Horizontally reflects rect location within
        frame coordinate system along line (x=frame_width/2)
        """
        # Calculate flipping axis as frame median
        flip_axis = frame_width/2

        # Determine whether or not rect overlaps the 
        #   flipping axis
        # If it does, calculate distance from axis 
        #   to right edge and reassign rect x-origin
        #   to axis minus that distance
        if flip_axis in range (self.x, self.right+1):
            offset = self.right - flip_axis
            self.x = flip_axis - offset

        # If no overlap, determine if rect lies to
        #   the left or the right of the axis
        else:
            if self.right < flip_axis:
                offset = flip_axis - self.right
                self.x = flip_axis + offset
            elif self.x > flip_axis:
                offset = self.x - flip_axis
                self.right = flip_axis - offset

class AnimationFrame(pyg.sprite.Sprite):
    """
    Class representing a frame of animation
    and its associated collision rects

    (Alternate implementation: Has multiple
    lists of rects separated by type flag.
    The idea is to minimize the number of 
    rects you have to iterate thru per
    frame and/or event to check for different
    types of collision.
    """
    def __init__(self, name, axis, image, rects):
        """
        Constructs an AnimationFrame from the
        image + RectWithType data passed in
        """
        super(AnimationFrame, self).__init__()
        self.image = image
        self.axis = axis
		
        # Total frame dimensions -- used to determine
        #   drawing coordinates
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

        self.name = name
        self.vuln_rects = []
        self.atk_rects = []

        # Sprite rect is always the first rect 
        #   member following the frame's name 
        # There is ONLY ever one sprite rect 
        #   per frame (I think; this may change)
        self.sprite_rect = rects[0]
        
        # Remaining rects are added to different
        #   lists based on their type flag
        for x in range (1, len(rects)):
            if rects[x].type == "Vuln":
                self.vuln_rects.append(rects[x])
            elif rects[x].type == "Atk":
                self.atk_rects.append(rects[x])
				
class SpriteSheet(object):
    """
    Class used to grab images out of a sprite sheet.
    """
    def __init__(self, file_name):
        """
        Construct a SpriteSheet from image at file 
        path (file_name) and convert
        """
        self.sprite_sheet = pyg.image.load(file_name).convert()
		
    def get_image(self, x, y, width, height):
        """
        Grab a single image out of the sprite_sheet image
        Parameters: (x,y) for origin of frame you wish to
        slice, and (width, height) for the dimensions of 
        your desired slice
        """
        image = pyg.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
		
        # Set transparency color key
        image.set_colorkey(con.ALPHA_COLOR)
		
        return image