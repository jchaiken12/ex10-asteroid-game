
import math

class Ship:

    def __init__(self, x, y, x_speed, y_speed, direction):

        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.dir = direction
        self.radius = 1
        self.size = 1

    def get_radius(self):
        return self.radius

    def get_size(self):
        return self.size

    def get_speed(self):
        return self.x_speed, self.y_speed

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def get_dir(self):
        return self.dir

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_dir(self, dir):
        self.dir = dir

    def set_speed(self, new_x_speed, new_y_speed):
        self.x_speed = new_x_speed
        self.y_speed = new_y_speed

    def has_intersection(self, obj):
        distance = math.sqrt((obj.getx() - self.x) ** 2 + (obj.gety() - self.y) ** 2)
        if distance <= obj.get_radius() + self.get_radius():
            return True
        return False
