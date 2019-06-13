from deltatimer import *
from mapper import *
from player import *

####

class MazeGame(object):
    """The actual game"""

    def __init__(self, maps, config):

        self.config = config
        self.dtimer = DeltaTimer(config.dt)
        self.mapper = Mapper(maps, config.width, config.height)
        self.fuelCount = self.mapper.act_map.countF()
        self.player_accel= config.player_accel
        self.friction = config.friction

        self.gatheredFuel = 0
        self.timeRatio = 1


    def reset(self, mode):

        self.text = ""
        self.mapper.select(mode)
        self.fuelCount = self.mapper.act_map.countF()
        x, y = self.mapper.get_point(*self.mapper.start)
        w, h =  self.mapper.player_sizehint
        size =  self.config.player_sizefac
        width = int(w * size)
        height = int(h * size)
        self.player = Player(x+1, y+1, width, height, self.config.player_color)

        self.gatheredFuel = 0
        self.timeRatio = 1


    def accelerate_player(self, events, accel):

        for ev in events:
            self.player.accelerate(ev, accel)


    def check_nextStage(self):

        if self.fuelCount <= 0 :
            return 'nextStage'

        return 'playing'


    def check_collision(self):
        """Check at first 4 sides of the player rectangle,
        if no collision occurs, check corners."""

        smap = self.mapper.act_map
        mapper = self.mapper

        ws = self.config.width_sensors
        hs = self.config.height_sensors
        north = [smap[mapper.get_cell(sx, sy)] == 'x'
                 for sx, sy in self.player.north_sensors(ws)]
        south = [smap[mapper.get_cell(sx, sy)] == 'x'
                 for sx, sy in self.player.south_sensors(ws)]
        east = [smap[mapper.get_cell(sx, sy)] == 'x'
                for sx, sy in self.player.east_sensors(hs)]
        west = [smap[mapper.get_cell(sx, sy)] == 'x'
                for sx, sy in self.player.west_sensors(hs)]

        west_east = any(west) or any(east)
        north_south = any(north) or any(south)

        if west_east or north_south:
            self.player.bounce(west_east, north_south)
            return True

        csx = False
        for sx, sy in self.player.vertex_sensors:
            if smap[mapper.get_cell(sx, sy)] == 'x':
                csx, csy = sx, sy
                break

        if not csx:
            return False

        old_px, old_py = self.player.oldpos
        px, py = self.player.pos
        old_csx = csx - px + old_px
        old_csy = csy - py + old_py

        old_cellx, old_celly = mapper.get_cell(old_csx, old_csy)
        cellx, celly = mapper.get_cell(csx, csy)
        self.player.bounce(abs(old_cellx - cellx) > 0, abs(old_celly - celly) > 0)

        return True


    def process(self, view, move_events):
        """Main method"""

        dur = view.frame_duration_secs
        #self.text = str(view.frame_duration_secs)

        if 'drag' in move_events:
            move_events.remove('drag')
            self.player.drag = True


        self.accelerate_player(move_events, dur * self.player_accel)
        self.dtimer += dur
        self.dtimer.integrate(self.transform_player, self.friction)
        self.check_drag()

        self.timeRatio -= 0.001

        self.mapper.draw_map(view)
        self.player.draw(view)
        self.draw_text(view)

        return self.check_nextStage()

    def check_drag(self):
        if not self.player.drag :
            return
        self.player.drag = False

        cell = self.mapper.get_cell(*self.player.center)
        place = self.mapper.act_map[cell]
        if place == 'f' and not self.player.loaded:
            self.mapper.act_map[cell] = '.'
            self.player.loaded = True

        if place == 'r' and self.player.loaded:
            self.mapper.act_map[cell] = 'o'
            self.gatheredFuel += self.mapper.act_map.intensityData[cell[0]][cell[1]] * self.timeRatio
            self.fuelCount -= 1
            self.player.loaded = False


    def transform_player(self, dt, friction):
        """Move player in 1 timestep dt."""

        self.player.move(dt, friction)
        collision = self.check_collision()
        if collision:
            self.player.restore_pos()
            self.player.move(dt, friction)


    def wait(self, view):
        """If player finds exit, ask for new game."""

        self.text = self.config.waiting_text
        self.draw_text(view)


    def draw_text(self, view):

        view.draw_text(self.text)


    def quit(self):

        print("Bye")
