
#imports
import arcade
import random
import math 
import numpy 

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_GAME_Height = 300
SCREEN_GAME_Width = 400
SCREEN_TITLE = "CS 230 Final Project!"


RECT_WIDTH = 50
RECT_HEIGHT = 50

NUMBER_OF_SHAPES = 20


class Shape:

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle
        self.color = color

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y
        self.angle += self.delta_angle


class Ellipse(Shape):

    def draw(self):
        arcade.draw_ellipse_filled(self.x, self.y, self.width, self.height,
                                   self.color, self.angle)


class Rectangle(Shape):

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
                                     self.color, self.angle)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.shape_list = None
        arcade.set_background_color(arcade.color.BOLE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shape_list = []

        for i in range(NUMBER_OF_SHAPES):
            x = random.randrange(0, SCREEN_GAME_Width)
            y = random.randrange(0, SCREEN_GAME_Height)
            width = random.randrange(10, 30)
            height = random.randrange(10, 30)
            angle = random.randrange(0, 360)

            d_x = random.randrange(-3, 4)
            d_y = random.randrange(-3, 4)
            d_angle = random.randrange(-3, 4)

            red = random.randrange(256)
            green = random.randrange(256)
            blue = random.randrange(256)
            alpha = random.randrange(256)

            shape_type = random.randrange(2)

            if shape_type == 0:
                shape = Rectangle(x, y, width, height, angle, d_x, d_y,
                                  d_angle, (red, green, blue, alpha))
            else:
                shape = Ellipse(x, y, width, height, angle, d_x, d_y,
                                d_angle, (red, green, blue, alpha))
            self.shape_list.append(shape)

    def on_update(self, dt):
        """ Move everything """

        for shape in self.shape_list:
            shape.move()

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        for shape in self.shape_list:
            shape.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()