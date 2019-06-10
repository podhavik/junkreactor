####

class GameMap(object):
    """Maze map representation"""

    def __init__(self, map_data):

        self.width = len(map_data[0])
        self.height = len(map_data)
        self.data = map_data


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

    def noF(self):

        for i, y in enumerate(self.data):
            for j, x in enumerate(y):
                if x == 'f':
                    return False
        return True



    @property
    def start(self):
        """Search the starting point, there should be only one."""

        for i, y in enumerate(self.data):
            for j, x in enumerate(y):
                if x == 's':
                    return j, i