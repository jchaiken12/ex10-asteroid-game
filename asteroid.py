
import math

class Asteroid:

    def __init__(self, x, y, x_speed, y_speed, size):

        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.size = size

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_radius(self):
        return self.size*10-5

    def has_intersection(self, obj):
        distance = math.sqrt((obj.getx() - self.x) ** 2 + (obj.gety() - self.y) ** 2)
        if distance <= obj.get_radius() + self.get_radius():
            return True
        return False
