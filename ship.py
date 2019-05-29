
import math

class Ship:

    def __init__(self, x, y, x_speed, y_speed, direction):

        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.dir = direction
        self.radius = 1

    def get_radius(self):
        return self.radius

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_dir(self, dir):
        self.dir = dir
