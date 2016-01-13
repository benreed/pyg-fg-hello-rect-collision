"""
Module for instantiated game objects 
subject to physics and/or state updates
Written Jan 11, 2016 by Benjamin Reed
Version 0.0.1-alpha
"""
import pygame as pyg
import constants as con

"""
TypedRect flag legend:
   "Sprite" : Rect is used to determine sprite collision
              and image penetration. For every frame 
              displayed, there is never more or less than
              one "Sprite" rect.
   "Vuln"   : Rect is used to determine what parts of 
              the displayed image can be hit by attacks.
              If an "Attack" rect collides with this
              rect, damage/hit state logic will be applied.
              Collision between two "Vuln" rects is ignored.
              Collision between "Vuln" and "Sprite" rects
              is ignored.
   "Atk"    : Rect is used to determine what parts of 
              the displayed image can hit "Vuln" type
              rects as an attack.
              Collision between two "Atk" rects will 
              probably be ignored, unless a cool/doable
              special case is suggested.
              Collision between "Atk" and "Sprite" rects
              will probably be ignored. 
"""

class TypedRect(pyg.Rect):
    """
    An extended Pygame rect with a type flag
    indicating what type of collision detection
    it is used for
    Used for basic, non-rotated AABB collision 
    """
    def __init__(self, type, x, y, width, height):
        """
        Calls Pygame rect superconstructor and adds an
        associated type value
        """
        super(TypedRect, self).__init__(x, y, width, height)
        self.type = type

class MovableObject(object):
    """
    A basic game object that can be moved on screen
    (has a deltaX and deltaY)
    Contains an indefinite number of TypedRects
    whose number, dimensions, and locations can be
    changed in a single update
    """
    def __init__(self):
        """
        Initializes deltaX and deltaY to 0
        """
        # Speed dimensions
        self.deltaX = 0
        self.deltaY = 0

        # Absolute spatial coordinates -- used as control
        #   rect's coords
        self.x = 50
        self.y = 50

        # Specific gravity
        self.gravity = 0
        
        # Collision rect members (initially empty)
        self.rects = []

        # Control rect -- defines character's absolute
        #   spatial area for sprite collision + penetration
        # Always flag as type "Sprite"
        self.control_rect = TypedRect("Sprite", self.x, self.y, 30, 50)
        self.rects.append(self.control_rect)

        # Current animation frame to display
        self.current_frame = None
        #self.drawing_rect = pyg.Rect(self.x, self.y, 30, 50)
        self.drawing_rect = TypedRect("Sprite", self.x, self.y, 30, 50)
        
    def apply_grav(self):
        """
        Applies object-specific gravity to
        deltaY
        """
        if self.deltaY == 0:
            self.deltaY = 1
        else:
            self.deltaY += self.gravity

    def land(self, floor):
        """
        Stops movement on y-axis, adjusts control
        rect to rest on top of floor, and adjusts 
        all other rect members to reflect
        (Use in: sprite collision)
        """
        self.stopY()
        self.control_rect.bottom = floor
        
    def moveX(self):
        """
        Moves all rect members on x axis by delta
        value
        """
        for rect in self.rects:
            rect.x += self.deltaX
        #self.drawing_rect.x += self.deltaX
    
    def moveY(self):
        """
        Moves all rect members on y axis by delta
        value
        """
        for rect in self.rects:
            rect.y += self.deltaY
        #self.drawing_rect.y += self.deltaY

    def stopX(self):
        """
        Stops horizontal movement of all rect members
        """
        self.deltaX = 0

    def stopY(self):
        """
        Stops vertical movement of all rect members
        """
        self.deltaY = 0
