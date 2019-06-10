#!/usr/bin/env python

####

class Grid(object):
    """Calculate points on a rectangular grid."""

    def __init__(self, dx=1, dy=1, xoff=0, yoff=0):

        self.dx = dx
        self.dy = dy
        self.xoff = xoff
        self.yoff = yoff


    def get_point(self, x, y):

        return self.xoff + x * self.dx, self.yoff + y * self.dy


    def get_rect(self, x, y):
        """Return rectangle parameters for pygame."""

        return self.get_point(x, y) + (self.dx, self.dy)


    def get_cell(self, x, y):
        """Snap coordinates to center point grid."""
        x = int(x+0.5)
        y = int(y+0.5)
        return (x-self.xoff+self.dx//2)//self.dx, (y-self.yoff+self.dy//2)//self.dy
