import pygame, pyjoycon as pyjc

class JoyControllerSingle(pyjc.GyroTrackingJoyCon,pyjc.PythonicJoyCon):
    def update(self):
        if self.battery_level < 2:
            print("Battery is low")