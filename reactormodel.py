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
        self.fuel = 0
        self.energyProduced = 0

        self.rodsControl = 1.0
        self.pumpControl = 0.0

        self.rodsPosition = 1.0
        self.rodsVelocity = 0.001

        self.reactorTemperature = 0
        self.turbineTemperature = 0
        self.reactorMaxTemp = 1500
        self.turbineMaxTemp = 400
        self.reactorEmergency = False
        self.turbineEmergency = False

        self.reactorCoolFactor = 0.0015
        self.turbineCoolFactor = 0.00062
        self.rodFactor = 0.005
        self.tempTransferFactor = 0.7
        self.tempToEnergyFactor = 0.001

        self.lastReactorRodesDelta = 0
        self.reactorRodesMomentumFactor = 0.996

    def control(self, events):
        for ev in events:
            if ev == 'up': self.rodsControl += 0.01
            if ev == 'down': self.rodsControl -= 0.01
            if ev == 'left': self.pumpControl -= 0.01
            if ev == 'right': self.pumpControl += 0.01

        if self.rodsControl < 0 : self.rodsControl = 0
        if self.pumpControl < 0 : self.pumpControl = 0
        if self.rodsControl > 1 : self.rodsControl = 1
        if self.pumpControl > 1 : self.pumpControl = 1


    def simulate(self, dt):
        self.fuel -= 0.1

        #override rods control in emergency
        if self.reactorEmergency :
            self.rodsControl = 1.0
            if self.reactorTemperature < self.reactorMaxTemp/2 :
                self.reactorEmergency = False

        #move rods
        positionDiff = self.rodsControl - self.rodsPosition
        if abs(positionDiff) > self.rodsVelocity :
            self.rodsPosition += math.copysign(self.rodsVelocity, positionDiff)

        #reactor momentum
        self.lastReactorRodesDelta = (1-self.rodsPosition)*self.rodFactor + \
                                     self.reactorRodesMomentumFactor*self.lastReactorRodesDelta

        #reactor is cooled by pumping to turbine
        reactorTurbineTempDiff = self.reactorTemperature-self.turbineTemperature
        reactorCooling = self.pumpControl*self.reactorCoolFactor*reactorTurbineTempDiff
        self.reactorTemperature += self.lastReactorRodesDelta - reactorCooling

        #turbine temp delta = heat from reactor - turbine cooling
        self.turbineTemperature += reactorCooling*self.tempTransferFactor - \
                                   self.turbineCoolFactor*self.turbineTemperature

        #trun off turbine in emergency
        if not self.turbineEmergency :
            self.energyProduced += self.turbineTemperature*self.tempToEnergyFactor

        if self.reactorTemperature < 0 :
            self.reactorTemperature = 0
        if self.turbineTemperature < 0 :
            self.turbineTemperature = 0

        if self.reactorTemperature > self.reactorMaxTemp :
            self.reactorEmergency = True
        if self.turbineTemperature > self.turbineMaxTemp :
            self.turbineEmergency = True
        else:
            self.turbineEmergency = False

    def isEnd(self):
        return self.fuel < 0

    def draw(self, view):
        view.draw_text('Rods control: ' + str(self.rodsControl), (0, 180, 0), 15, (20, 60))
        view.draw_text('Pump control: ' + str(self.pumpControl), (0, 180, 0), 15, (20, 100))

        view.draw_text('Rods position: ' + str(round(self.rodsPosition, 2)), (0, 180, 0), 15, (370, 60))


        degree = u'\N{DEGREE SIGN}'

        view.draw_text('Reactor Temp: ' + str(round(self.reactorTemperature, 1)) + degree + 'C',
                       (0, 180, 0), 15, (20, 130))
        view.draw_text('Turbine Temp: ' + str(round(self.turbineTemperature, 1)) + degree + 'C',
                       (0, 180, 0), 15, (20, 170))
        view.draw_text('MAX: ' + str(self.reactorMaxTemp) ,
                       (0, 180, 0), 15, (270, 130))
        view.draw_text('MAX: ' + str(self.turbineMaxTemp),
                       (0, 180, 0), 15, (270, 170))

        view.draw_text('Energy produced: ' + str(round(self.energyProduced, 0)),
                       (0, 180, 0), 15, (20, 210))

        if self.reactorEmergency :
            view.draw_text('REACTOR EMERGENCY - rods control disabled', (200, 0, 0), 15, (20, 250))

        if self.turbineEmergency :
            view.draw_text('TURBINE OVERHEATED - power generation disabled', (200, 0, 0), 15, (20, 290))

        view.rectangle([20,20,20,20], mapcolors['d'], 0)
        view.rectangle([200, 60, 160, 10], mapcolors['f'], 1)
        view.rectangle([200, 60, 160*self.rodsControl, 10], mapcolors['f'], 0)
        view.rectangle([200, 100, 160 , 10], mapcolors['f'], 1)
        view.rectangle([200, 100, 160*self.pumpControl, 10], mapcolors['f'], 0)
