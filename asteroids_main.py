from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys
import random
import math

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        ship_x = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
        ship_y = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
        self.__screen.draw_ship(ship_x, ship_y, 0)
        self.__player = Ship(ship_x, ship_y, 0, 0, 0)

        ast_speeds = list(range(-4, 0)) + list(range(1, 5))
        ast_xs, ast_ys = self.non_colliding_start(self.__player, asteroids_amount)
        self.__ast_size = 3
        self.__ast_ls =[]
        for i in range(asteroids_amount):
            as_x_sp = random.choice(ast_speeds)
            as_y_sp = random.choice(ast_speeds)
            asteroid = Asteroid(ast_xs[i], ast_ys[i], as_x_sp, as_y_sp, self.__ast_size)
            self.__ast_ls.append(asteroid)
            self.__screen.register_asteroid(asteroid, self.__ast_size)
            self.__screen.draw_asteroid(asteroid, ast_xs[i], ast_ys[i])

        self.__life_count = 0
        self.__score = 0
        self.__torpedo_ls = []

    #TODO must also check ship size to be sure asteroid is not intersecting that as well
    def non_colliding_start(self, ship, asteroids_amount):
        """

        This will return a list of coordinates where the player is not hitting the
        any of the asteroids at the start of creating the game.

        :param ship: is the player
        :param asteroids_amount: the number of asteroids
        :return:
        """

        MAX_X = self.__screen_max_x
        MAX_Y = self.__screen_max_y
        MIN_X = self.__screen_min_x
        MIN_Y = self.__screen_min_y

        ast_xs = []
        ast_ys = []
        ast_size = 3 # todo make the call to contant called the size
        sh_size = self.__player.get_size()
        # ensure there are no collisions of asteroids and the player
        while len(ast_xs) <= asteroids_amount or len(ast_ys) <= asteroids_amount:
            x = random.randint(MIN_X, MAX_X)
            if x not in list(range(ship.getx() - ast_size, ship.getx() + ast_size+1)) \
                    and len(ast_xs) <= asteroids_amount:
                ast_xs.append(x)
            y = random.randint(MIN_Y, MAX_Y)
            if y not in list(range(ship.gety() - ast_size, ship.gety() + ast_size+1)) \
                    and len(ast_ys) <= asteroids_amount:
                ast_ys.append(y)

        return ast_xs, ast_ys

    def move(self, obj):
        axis_delta = self.__screen_max_x - self.__screen_min_x
        new_x = (obj.x_speed + obj.getx() - self.__screen_min_x) % axis_delta + self.__screen_min_x
        new_y = (obj.y_speed + obj.gety() - self.__screen_min_y) % axis_delta + self.__screen_min_y
        obj.set_x(new_x)
        obj.set_y(new_y)

    def move_dir(self, ship, turn_left, turn_right):

        if turn_left: ship.set_dir(ship.dir + 7)
        elif turn_right: ship.set_dir(ship.dir - 7)

    def speed_up(self, ship, up_pressed):

        if up_pressed:
            heading_rad = math.radians(ship.dir)
            x_speed = ship.get_speed()[0] + math.cos(heading_rad)
            y_speed = ship.get_speed()[1] + math.sin(heading_rad)
            ship.set_speed(x_speed, y_speed)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def shoot(self, ship):

        space_pressed = self.__screen.is_space_pressed()

        if space_pressed:
            ship_dir = math.radians(ship.get_dir())
            x_speed = ship.get_speed()[0] + 2*math.cos(ship_dir)
            y_speed = ship.get_speed()[1] + 2*math.sin(ship_dir)
            torpedo = Torpedo(ship.getx(),ship.gety(), x_speed, y_speed, ship.get_dir())
            self.__screen.register_torpedo(torpedo)
            self.__screen.draw_torpedo(torpedo, ship.getx(),ship.gety(), ship.get_dir())
            self.__torpedo_ls.append(torpedo)

    def split_ast(self, ast):
        pass

    def _game_loop(self):
        # Your code goes here
        ship = self.__player
        left = self.__screen.is_left_pressed()
        right = self.__screen.is_right_pressed()
        up_pressed = self.__screen.is_up_pressed()

        self.move_dir(ship, left, right)
        self.move(ship)

        self.speed_up(ship, up_pressed)
        self.__screen.draw_ship(ship.x, ship.y, ship.dir)
        self.shoot(ship)

        for i in range(len(self.__torpedo_ls)):
            tor = self.__torpedo_ls[i]
            self.move(tor)
            self.__screen.draw_torpedo(tor, tor.getx(),tor.gety(), tor.get_dir())

        i = 0
        while i <= len(self.__ast_ls)-1:
            asteroid = self.__ast_ls[i]
            self.move(asteroid)
            self.__screen.draw_asteroid(asteroid, asteroid.getx(), asteroid.gety())

            if asteroid.has_intersection(ship) and ship.has_intersection(asteroid) \
                    and self.__life_count <= 2:
                self.__screen.show_message('You messed up', 'get better kid and maybe you get a popsicle')
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(asteroid)
                del self.__ast_ls[i]
                self.__life_count = self.__life_count + 1
            i = i + 1

        for tor in self.__torpedo_ls:
            j = 0
            while j <= len(self.__ast_ls) - 1:
                ast = self.__ast_ls[j]
                if tor.has_intersection(ast) and ast.has_intersection(tor):
                    if ast.get_size() == 3:
                        self.__score += 20
                        self.split_ast(ast)
                    elif ast.get_size() == 2:
                        self.__score += 50
                    elif ast.get_size == 1:
                        self.__score += 100
                        del self.__ast_ls[j]
                    self.__screen.set_score(self.__score)
                j += 1




def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
