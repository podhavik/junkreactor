####

from gameconstants import *
from gamemap import *
from grid import *

import copy
import random


mapcolors = \
    {'x': (100, 60, 30),
     'd': (30, 120, 10),
     'u': (30, 190, 10),
     'r': (150, 0, 0),
     'f': (0, 0, 250),
     'e': (250, 0, 0)}


class Mapper(object):
    """Manage all maps."""

    def __init__(self, maps, width, height):

        self.view_width = width
        self.view_height = height
        self.originalData = []
        #for m in maps :
            #self.originalData.append(copy.deepcopy(m))
            #for i in m :

            #self.originalData.append([i[:] for i in m ])
        #self.originalData = [''.join(i) for m in maps for i in m ]
        self.originalData = copy.deepcopy(maps)
        self.maps = [GameMap(m) for m in maps]


    def select(self, mode=START):

        assert mode in (START, UP, DOWN, RANDOM), "wrong selection"

        n = len(self.maps)
        if mode == START:
            self.act_index = 0
            data = copy.deepcopy(self.originalData)
            self.maps = [GameMap(m) for m in data]
        elif mode == RANDOM:
            if len(self.maps) > 1:
                self.act_index = random.choice(list(set(range(n)) - set((self.act_index,))))
        else:
            self.act_index = (self.act_index + n + mode) % len(self.maps)

        self.act_grid, self.act_center_grid = self.adjust_grids()
        return self.act_map, self.act_grid, self.act_center_grid


    def adjust_grids(self):
        """There are 2 sorts of grids:
        a grid for the upper left Corner for drawing rectangles,
        a grid for their center points, which are used for collision detection."""

        smap = self.act_map
        w = self.view_width // smap.width - 1
        h = self.view_height // smap.height - 1
        xoff = self.view_width - smap.width * w
        yoff = self.view_height - smap.height * h
        grid = Grid(w, h, xoff//2, yoff//2)
        # +1 !
        center_grid = Grid(w, h, xoff//2 + w//2 + 1, yoff//2 + h//2 + 1)

        return grid, center_grid


    def draw_map(self, view):

        smap = self.act_map
        grid = self.act_grid
        width = smap.width

        for y in range(smap.height):
            for x in range(width):
                place = smap[x, y]
                if place not in NOT_DRAWABLES:
                    #view.rectangle(grid.get_rect(x, y), mapcolors[place], place in PLACES)
                    view.rectangle(grid.get_rect(x, y), mapcolors[place], 0)


    @property
    def act_map(self):

        return self.maps[self.act_index]


    @property
    def start(self):

        return self.act_map.start


    def get_point(self, x, y):

        return self.act_grid.get_point(x, y)


    def get_rect(self, x, y):

        return self.act_grid.get_rect(x, y)


    def get_cell(self, x, y):

        return self.act_center_grid.get_cell(x, y)


    @property
    def player_sizehint(self):

        return self.act_grid.dx // 2, self.act_grid.dy // 2
