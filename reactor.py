#!/usr/bin/env python

"""
reactor.py

Nuclear reactor simulator.

Based on: (tile_based.py)
URL:     http://thepythongamebook.com/en:part2:pygame:step009
Author:  yipyip
"""

#Only needed for Python 2.x.
from __future__ import print_function, division

####

import pygame

import math

from pygview import *
from gameconstants import *
from controller import *

#### configuration


config = \
    {'fullscreen': False,
     'visibmouse': False,
     'width': 800,
     'height': 600,
     'back_color': (0, 0, 0),
     #'back_color': (230, 180, 40),
     'font_ratio': 8,
     'font_color': (255, 255, 255),
     'fps': 100,
     'dt': 0.01,
     'friction': 0.987,
     'player_sizefac': 1.2,
     'player_color': (255, 0, 255),
     'player_accel': 300,
     'width_sensors': 8,
     'height_sensors': 8,
     'title': "Maze Wanderer   (Move with Cursor Keys, press Esc to exit)",
     'waiting_text': "quit=Esc, again=Other Key"}

#### maps
# x = wall
# s = start
# d = level down
# u = level up
# r = random level



# 5 x 8
test_map= \
    ["xxxxx",
     "xs..x",
     "x..ux",
     "x..dx",
     "x..rx",
     "x..ex",
     "x...x",
     "xxxxx"]

reactor_test = \
    ["xxxxxxxxxxxxxxxxxxxxxxxxxx",
     "xsf......................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x............r...........x",
     "x...........rrr..........x",
     "x..........rrrrr.........x",
     "x...........rrr..........x",
     "x............r...........x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "xxxxxxxxxxxxxxxxxxxxxxxxxx"]

reactor_map = \
    ["xxxxxxxxxxxxxxxxxxxxxxxxxx",
     "xs.......................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x............r...........x",
     "x...........rrr..........x",
     "x..........rrrrr.........x",
     "x...........rrr..........x",
     "x............r...........x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x........................x",
     "x...f...f...f...f...f....x",
     "x........................x",
     "xxxxxxxxxxxxxxxxxxxxxxxxxx"]


# game maps
#maps =  easy_map, medium_map, hard_map

# testing
maps = reactor_test, reactor_map
# maps = test_map, easy_map, medium_map, hard_map


####

class Config(object):
    """Change dictionary to object attributes."""

    def __init__(self, **kwargs):

        self.__dict__.update(kwargs)

####

def main():

    Controller(PygView, maps, Config(**config)).run()

####

if __name__ == '__main__':

    main()
