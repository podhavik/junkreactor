from deltatimer import *
from reactormodel import *


class ReactorGame(object):
    """The actual game"""

    def __init__(self, config):

        self.config = config
        self.dtimer = DeltaTimer(config.dt)
        self.reactorModel = ReactorModel()


    def reset(self, mode):

        self.text = ""


    def process(self, view, move_events):
        """Main method"""

        dur = view.frame_duration_secs
        #self.text = str(view.frame_duration_secs)

        if 'drag' in move_events:
            move_events.remove('drag')
            #return 'ending'

        self.reactorModel.control(move_events)
        self.dtimer += dur
        self.dtimer.integrate(self.reactorModel.simulate)

        if self.reactorModel.isEnd() :
            return 'ending'

        self.reactorModel.draw(view)
        self.text = 'Fule: ' + str(round(self.reactorModel.fuel,1))
        self.draw_text(view)

        return 'playing'


    def wait(self, view):
        """If player finds exit, ask for new game."""

        self.text = self.config.waiting_text
        self.draw_text(view)


    def draw_text(self, view):

        view.draw_text(self.text)


    def quit(self):

        print("Bye")
