####
import numpy as np
import random

class GameMap(object):
    """Maze map representation"""

    def __init__(self, map_data):

        self.width = len(map_data[0])
        self.height = len(map_data)
        self.data = map_data
        self.intensityData = [[0 for x in range(self.width)] for y in range(self.height)]
        #TODO implement own method
        size = max(self.width, self.height)

        fwhm = 8
        center = [self.width/2, self.height/2]

        gaus = self.makeGaussian(size, fwhm, [center[0]+3, center[1]+3])
        gaus2 = self.makeGaussian(size, fwhm, [center[0]-3, center[1]-3])

        for i in range(len(gaus)):
            for j in range(len(gaus[i])):
                gaus[i][j] += gaus2[i][j]

        #TODO do better randomization
        self.intensityData = [[gaus[x][y]*200 + random.randint(1,6) for x in range(self.width)] for y in range(self.height)]
        self.intensityData = self.intensityData


    def __getitem__(self, xy):
        x = xy[0]
        y = xy[1]
        return self.data[y][x]

    def __setitem__(self, xy, value):
        x = xy[0]
        y = xy[1]
        l = list(self.data[y])
        l[x] = value
        self.data[y] = ''.join(l)

    def makeGaussian(self, size, fwhm = 3, center = None):
        """Make a square gaussian kernel.

        :param size: length of a side of the square
        fwmh is full-width-half-maximum, which
        can be thought of as an effective radius
        :param fwhm:
        :param center:
        :return:
        """
        x = np.arange(0, size, 1, float)
        y = x[:, np.newaxis]

        if center is None:
            x0 = y0 = size // 2
        else:
            x0 = center[0]
            y0 = center[1]

        return np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)

    def countF(self):
        fCount = 0
        for i, y in enumerate(self.data):
            for j, x in enumerate(y):
                if x == 'f':
                    fCount += 1
        return fCount



    @property
    def start(self):
        """Search the starting point, there should be only one."""

        for i, y in enumerate(self.data):
            for j, x in enumerate(y):
                if x == 's':
                    return j, i