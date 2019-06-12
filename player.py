####

class Player(object):
    """Representation of the moving player rectangle"""

    dirs = {'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)}

    sensor_pts = ((0, 0), (1, 0), (1, 1), (0, 1))

    def __init__(self, x, y, width, height, color):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.width2 = width // 2
        self.height2 = height // 2
        self.color = color
        self.dx = 0
        self.dy = 0
        self.drag = False
        self.loaded = False

    # @property
    # def drag(self):
    #
    #     return self.drag

    @property
    def pos(self):

        return self.x, self.y


    @property
    def oldpos(self):

        return self.xold, self.yold


    def restore_pos(self):

        self.x, self.y = self.oldpos


    @property
    def center(self):

        x, y = self.pos
        return x + self.width2, y + self.height2


    def move(self, dt, friction):

        self.dx *= friction
        self.dy *= friction
        self.xold, self.yold = self.pos
        self.x += self.dx * dt
        self.y += self.dy * dt


    def accelerate(self, direct, acc):

        xdir, ydir = Player.dirs[direct]
        self.accx = xdir * acc
        self.accy = ydir * acc
        self.dx += self.accx
        self.dy += self.accy


    @property
    def vertex_sensors(self):

        x, y = self.pos
        return [(x + sx * self.width, y + sy * self.height) for sx, sy in Player.sensor_pts]


    def north_sensors(self, n):

        x, y = self.pos
        delta = self.width // n
        return [(x + i * delta, y) for i in range(1, n)]


    def south_sensors(self, n):

        x, y = self.pos
        delta = self.width // n
        h = y + self.height
        return [(x + i * delta, h) for i in range(1, n)]


    def west_sensors(self, n):

        x, y = self.pos
        delta = self.height // n
        return [(x, y + i * delta) for i in range(1, n)]


    def east_sensors(self, n):

        x, y = self.pos
        delta = self.height // n
        w = x + self.width
        return [(w, y + i * delta) for i in range(1, n)]


    def bounce(self, west_east, north_south):

        self.dx = (self.dx, -self.dx)[west_east]
        self.dy = (self.dy, -self.dy)[north_south]


    def draw(self, view):

        view.rectangle((self.x, self.y, self.width, self.height), self.color)
        if self.loaded :
            view.rectangle((self.x+self.width/4, self.y+self.height/4, self.width/2, self.height/2), (0, 0, 130))
