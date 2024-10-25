import pygame as pg
import time
import sys

from pygame.math import Vector2 as vec2
from define import WIN_W, WIN_H
from grid import Grid

class Game:
    def __init__(self):
        """
        This method define all variables needed by the program
        """
        # Start of pygame
        pg.init()

        # We remove the toolbar of the window's height
        self.winSize = vec2(WIN_W, WIN_H)
        # We create the window
        self.win = pg.display.set_mode(self.winSize, pg.RESIZABLE)

        self.clock = pg.time.Clock() # The clock be used to limit our fps
        self.fps = 0

        self.last = time.time()

        self.onFocus = True

        self.runMainLoop = True

        self.grid = Grid()


    def run(self):
        """
        This method is the main loop of the game
        """
        # Game loop
        while self.runMainLoop:
            self.input()
            self.tick()
            self.render()
            self.clock.tick(self.fps)


    def input(self):
        """
        The method catch user's inputs, as key presse or a mouse click
        """
        # We check each event
        self.mouseScrollState = 0
        self.keyDown = []

        for event in pg.event.get():
            # If the event it a click on the top right cross, we quit the game
            if event.type == pg.QUIT:
                self.quit()

            elif event.type == pg.WINDOWSIZECHANGED:
                self.winSize = vec2(self.win.get_size())

            elif event.type == pg.WINDOWFOCUSGAINED:
                self.onFocus = True

            elif event.type == pg.WINDOWFOCUSLOST:
                self.onFocus = False

            elif event.type == pg.MOUSEWHEEL:
                self.mouseScrollState = event.y

            elif event.type == pg.KEYDOWN:
                self.keyDown.append(event.key)

        self.keyboardState = pg.key.get_pressed()
        self.mouseState = pg.mouse.get_pressed()
        self.mousePos = pg.mouse.get_pos()

        # Press espace to quit
        if self.keyboardState[pg.K_ESCAPE]:
            self.quit()


    def tick(self):
        """
        This is the method where all calculations will be done
        """
        tmp = time.time()
        delta = tmp - self.last
        self.last = tmp

        # Zoom management
        if self.mouseScrollState == 1:
            self.grid.zoomOut()
        elif self.mouseScrollState == -1:
            self.grid.zoomIn()

        # Modify draw config
        if pg.K_b in self.keyDown:
            self.grid.switchDrawTileBorder()

        # Camera movement
        if self.keyboardState[pg.K_UP]:
            self.grid.moveOffset('u')
        elif self.keyboardState[pg.K_DOWN]:
            self.grid.moveOffset('d')
        if self.keyboardState[pg.K_LEFT]:
            self.grid.moveOffset('l')
        elif self.keyboardState[pg.K_RIGHT]:
            self.grid.moveOffset('r')

        # Change tile status
        if self.mouseState[0]:
            self.grid.handleMouseClick(self.mousePos, 1)

        elif self.mouseState[2]:
            self.grid.handleMouseClick(self.mousePos, 0)

        if self.keyboardState[pg.K_SPACE]:
            self.grid.clear()

        pg.display.set_caption(f"fps : {self.clock.get_fps():.2f}")


    def render(self):
        """
        This is the method where all graphic update will be done
        """
        # We clean our screen with one color
        self.win.fill((0, 0, 0))

        self.grid.draw(self.win)

        # We update the drawing.
        # Before the function call, any changes will be not visible
        pg.display.update()


    def quit(self):
        """
        This is the quit method
        """
        # Pygame quit
        pg.quit()
        sys.exit()


print("COMMANDS :")
print(" - mouse wheel UP -> zoom in grid")
print(" - mouse wheel DOWN -> zoom out grid")
print(" - key B -> enable / disable drawing of tiles' border")
print(" - key UP -> move grid down")
print(" - key DOWN -> move grid up")
print(" - key LEFT -> move grid right")
print(" - key RIGHT -> move grid left")
print(" - key SPACE -> clear grid")


Game().run() # Start game
