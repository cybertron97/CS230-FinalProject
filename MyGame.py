#imports
import arcade
import random
import math 
import os 
import timeit
import threading
import time

from tkinter import *
from tkinter.ttk import *
import tkinter as tk

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_GAME_Height = 300
SCREEN_GAME_Width = 400
SCREEN_TITLE = "CS 230 Final Project!"

SQUARE_LENGTH = 20

NUMBER_OF_SHAPES = 1
lastChoice = "Right"

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

class RectangleOutline(Shape):
    def draw(self):
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height,
                                     self.color, 3)
class Line(Shape):
    def draw(self):
        newX = 25 * math.cos(self.angle * math.pi / 180)
        newY = 25 * math.sin(self.angle * math.pi / 180)
        arcade.draw_line(self.x, self.y, self.x + newX, self.y + newY, self.color, 3)
        arcade.draw_ellipse_filled(self.x + newX, self.y + newY, 10, 10, self.color, 3)
        
class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.join(os.path.dirname(__file__))
        os.chdir(file_path)
        self.shape_list = None
        arcade.set_background_color(arcade.color.BOLE)
        self.size = 100
        self.isRunning = False

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shape_list = []

        x = random.randrange(SQUARE_LENGTH, SCREEN_WIDTH - SQUARE_LENGTH)
        y = SQUARE_LENGTH / 2

        base = Rectangle(x, y, SQUARE_LENGTH, SQUARE_LENGTH, 0, 0, 0, 0, arcade.color.YELLOW)
        self.shape_list.append(base)
        
        line = Line(x, y, 0, 0, 0, 0, 0, 0, arcade.color.BLACK)
        self.shape_list.append(line)

        if(x > SCREEN_WIDTH - x):
            self.targetX = random.randrange(int(self.size / 2), int(x - SQUARE_LENGTH - self.size / 2))
        else:
            self.targetX = random.randrange(int(x + SQUARE_LENGTH + self.size / 2), int(SCREEN_WIDTH - self.size / 2))
        targetY = self.size / 2
            
        zone = RectangleOutline(self.targetX, targetY, self.size, self.size, 0, 0, 0, 0, arcade.color.RED)
        self.shape_list.append(zone)

    def update_line(self, linVel, angVel):
        line = self.shape_list[1]
        line.angle = angVel
        self.linearVelocity = linVel
        
    def reflect_line(self):
        global lastChoice
        line = self.shape_list[1]
        while line.angle < 0:
            line.angle = line.angle + 360
        angle = line.angle % 360
        if lastChoice == "Left" and (angle <= 90 or angle >= 270):
            line.angle = (line.angle + 180)
        if lastChoice == "Right" and (angle >= 90 and angle <= 270):
            line.angle = (line.angle + 180)
        #line.angle = -1 * line.angle

    def simulate_ball(self):
        self.isRunning = True
        self.t = 0
        self.oldX = self.shape_list[0].x
        self.oldY = self.shape_list[0].y
        
    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        for shape in self.shape_list:
            if(self.isRunning == True):
                angle = self.shape_list[1].angle * math.pi / 180
                self.shape_list[0].x = self.linearVelocity * math.cos(angle) * self.t + self.shape_list[1].x
                self.shape_list[0].y = -16*self.t*self.t + (self.linearVelocity * math.sin(angle) * self.t) + SQUARE_LENGTH
                self.t = self.t + 0.01
                if(self.shape_list[0].y <= 5):
                    if(self.shape_list[0].x >= self.targetX + SQUARE_LENGTH / 2 - self.size / 2 and self.shape_list[0].x <= self.targetX - SQUARE_LENGTH / 2 + self.size / 2):
                        self.size = int(math.floor(self.size * 0.9))
                        self.setup()
                    else:
                        self.shape_list[0].x = self.oldX
                        self.shape_list[0].y = self.oldY
                    self.isRunning = False
            if(self.isRunning == False or not isinstance(shape, Line)):
                shape.draw()

def selectOption():
    global angVelRButton, gameWindow, lastChoice
    if(angVelRButton.get() != "" and angVelRButton.get() != lastChoice):
        lastChoice = angVelRButton.get()
        gameWindow.reflect_line()

def onPlayClick():
    global gameWindow
    gameWindow.simulate_ball()

def onChange(evt):
    global linVelEntry, angVelEntry, gameWindow
    if(linVelEntry.get() == '' or math.isnan(int(linVelEntry.get()))):
        linVel = 0
    else:
        linVel = int(linVelEntry.get())
    if(angVelEntry.get() == '' or math.isnan(int(angVelEntry.get()))):
        ang = 0
    else:
        ang = int(angVelEntry.get())
    gameWindow.update_line(linVel, ang)
    
def onExitClick():
    global buttonWindow, gameWindow
    buttonWindow.destroy()
    arcade.close_window()

def createWindow(app):
    global angVelRButton, linVelEntry, angVelEntry
    app.columnconfigure(5)
    lengths = [2, 15, 1, 15, 2]
    for i in range(0,len(lengths)):
        Label(app, text=' ', width=lengths[i]).grid(row=0, column=i)
        
    Label(app, text='Starting Linear Velocity:').grid(row=1, column=1)
    linVelEntry = Entry(app)
    linVelEntry.grid(row=1, column=3)
    linVelEntry.bind("<KeyRelease>", onChange)
    
    for i in range(0,len(lengths)):
        Label(app, text=' ', width=lengths[i]).grid(row=2, column=i)
        
    Label(app, text='Starting Angle:').grid(row=3, column=1)
    angVelEntry = Entry(app)
    angVelEntry.grid(row=3, column=3)
    angVelEntry.bind("<KeyRelease>", onChange)
    
    for i in range(0,len(lengths)):
        Label(app, text=' ', width=lengths[i]).grid(row=4, column=i)
        
    Label(app, text='Velocity Direction:').grid(row=5, column=1)
    Types = ["Left", "Right"]
    angVelRButton = StringVar()
    for i in range(0,len(Types)):
        text = Types[i]
        Radiobutton(app, text=text, variable=angVelRButton, value=text, command=selectOption).grid(row=6, column=2*i+1)
         
    for i in range(0,len(lengths)):
        Label(app, text=' ', width=lengths[i]).grid(row=7, column=i)
        
    playButton = Button(app, text='Play', command=onPlayClick)
    playButton.grid(row=8, column=1)
    closeButton = Button(app, text='Exit', command=onExitClick)
    closeButton.grid(row=8, column=3)
    
    app.geometry("320x200")
    app.mainloop()

def handleWindow():
    global buttonWindow
    buttonWindow = tk.Tk(className='CS 230 Final Project')
    createWindow(buttonWindow)

def main():
    global gameWindow
    buttonWindow = threading.Thread(target=handleWindow)
    buttonWindow.start()
    gameWindow = MyGame()
    gameWindow.setup()
    arcade.run()

if __name__ == "__main__":
    main()
