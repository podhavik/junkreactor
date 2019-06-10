####

class DeltaTimer(object):
    """Timing control"""

    def __init__(self, dt):

        self.dt = dt
        self.accu = 0.0


    def __iadd__(self, delta):

        self.accu += delta
        return self


    def integrate(self, func, *args):
        """For a fixed timestep dt, adjust movement to fps."""
        while self.accu >= self.dt:
            func(self.dt, *args)
            self.accu -= self.dt