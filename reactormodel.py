from gameconstants import *

import math

mapcolors = \
    {'x': (100, 60, 30),
     'd': (30, 120, 10),
     'u': (30, 190, 10),
     'r': (150, 0, 0),
     'f': (0, 0, 254),
     'e': (250, 0, 0)}

class ReactorModel(object):
    """Manage all maps."""

    def __init__(self):
        self.rodsControl = 1.0
        self.pumpControl = 0.0
        self.reactorTemperature = 0
        self.turbineTemperature = 0
        self.fuel = 0
        self.generatorOutput = 0

        self.reactorCoolFactor = 0.0009
        self.turbineCoolFactor = 0.00065
        self.rodFactor = 0.005
        self.tempTransferFactor = 0.5

        self.lastReactorRodesDelta = 0

    def control(self, events):
        for ev in events:
            if ev == 'up': self.rodsControl += 0.01
            if ev == 'down': self.rodsControl -= 0.01
            if ev == 'left': self.pumpControl += 0.01
            if ev == 'right': self.pumpControl -= 0.01

        if self.rodsControl < 0 : self.rodsControl = 0
        if self.pumpControl < 0 : self.pumpControl = 0
        if self.rodsControl > 1 : self.rodsControl = 1
        if self.pumpControl > 1 : self.pumpControl = 1


    def simulate(self, dt):
        self.fuel -= 0.1

        self.lastReactorRodesDelta = (1-self.rodsControl)*self.rodFactor + 0.993*self.lastReactorRodesDelta
        reactorTurbineTempDiff = self.reactorTemperature-self.turbineTemperature
        reactorCooling = self.pumpControl*self.reactorCoolFactor*reactorTurbineTempDiff
        self.reactorTemperature += self.lastReactorRodesDelta - reactorCooling

        self.turbineTemperature += reactorCooling*self.tempTransferFactor - self.turbineCoolFactor*self.turbineTemperature

        if self.reactorTemperature < 0 :
            self.reactorTemperature = 0
        if self.turbineTemperature < 0 :
            self.turbineTemperature = 0

    def isEnd(self):
        return self.fuel < 0

    def draw(self, view):
        view.draw_text('Rods: ' + str(self.rodsControl), (0, 180, 0), 15, (20, 60))
        view.draw_text('Pump: ' + str(self.pumpControl), (0, 180, 0), 15, (20, 100))


        degree = u'\N{DEGREE SIGN}'

        view.draw_text('Reactor Temp: ' + str(round(self.reactorTemperature,1)) + degree + 'C', (0, 180, 0), 15, (20, 130))
        view.draw_text('Turbine Temp: ' + str(round(self.turbineTemperature,1)) + degree + 'C', (0, 180, 0), 15, (20, 170))

        view.rectangle([20,20,20,20], mapcolors['d'], 0)
        view.rectangle([130, 60, 160, 10], mapcolors['f'], 1)
        view.rectangle([130, 60, 160*self.rodsControl, 10], mapcolors['f'], 0)
        view.rectangle([130, 100, 160 , 10], mapcolors['f'], 1)
        view.rectangle([130, 100, 160*self.pumpControl, 10], mapcolors['f'], 0)
