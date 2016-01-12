"""
Module for instantiated game objects 
subject to physics and/or state updates
Written Jan 11, 2016 by Benjamin Reed
Version 0.0.1-alpha
"""
import pygame as pyg
import constants as con

class TypedRect(pyg.Rect):
    """
    An extended Pygame rect with a type flag
    indicating what type of collision detection
    it is used for
    Used for basic, non-rotated AABB collision 
    """
    def __init__(self, type, x, y, width, height):
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
        self.deltaX = 0
        self.deltaY = 0
        self.x = 50
        self.y = 50
        self.gravity = 0
        self.rects = []
        
    def apply_grav(self):
        if self.deltaY == 0:
            self.deltaY = 1
        else:
            self.deltaY += self.gravity
        
    def moveX(self):
        """
        Moves all rect members on x axis by delta
        value
        """
        for rect in self.rects:
            rect.x += self.deltaX
    
    def moveY(self):
        """
        Moves all rect members on y axis by delta
        value
        """
        for rect in self.rects:
            rect.y += self.deltaY