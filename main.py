import pygame as pg
import time
import sys

from pygame.math import Vector2 as vec2
from define import  WIN_W, WIN_H,\
                    MIN_SIMULATION_SLEEP, MAX_SIMULATION_SLEEP, START_SIMULATION_SLEEP,\
                    SIMULATION_SPEED, FPS_CAP, MAX_FPS_CAP
from grid import    Grid

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
        self.fps = MAX_FPS_CAP

        self.last = time.time()

        self.onFocus = True

        self.runMainLoop = True

        self.grid = Grid()
        self.runSimulation = False
        self.simulationSleep = START_SIMULATION_SLEEP
        self.simulationSleepRemain = 0

        self.waitSimulationSpeedChange = 0
        self.waitFpsPrint = 0


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
        if self.keyboardState[pg.K_w] or self.keyboardState[pg.K_z]:
            self.grid.moveCamera('u', delta)
        elif self.keyboardState[pg.K_s]:
            self.grid.moveCamera('d', delta)
        if self.keyboardState[pg.K_a] or self.keyboardState[pg.K_q]:
            self.grid.moveCamera('l', delta)
        elif self.keyboardState[pg.K_d]:
            self.grid.moveCamera('r', delta)

        # Change tile status
        if self.mouseState[0]:
            self.grid.handleMouseClick(self.mousePos, 1)

        elif self.mouseState[2]:
            self.grid.handleMouseClick(self.mousePos, 0)

        # Clear grid
        if self.keyboardState[pg.K_c]:
            self.grid.clear()

        # Add tile at random position
        if self.keyboardState[pg.K_r]:
            self.grid.addRandomTile()

        # Change simulation run status
        if pg.K_SPACE in self.keyDown:
            self.runSimulation = not self.runSimulation

        # Change simulation speed
        if self.waitSimulationSpeedChange <= 0:
            if self.keyboardState[pg.K_LEFT]: # decrease simulation speed
                self.simulationSleep = min(MAX_SIMULATION_SLEEP,
                                        self.simulationSleep + SIMULATION_SPEED)
                self.waitSimulationSpeedChange = 0.2

            elif self.keyboardState[pg.K_RIGHT]: # increase simulation speed
                self.simulationSleep = max(MIN_SIMULATION_SLEEP,
                                        self.simulationSleep - SIMULATION_SPEED)
                self.waitSimulationSpeedChange = 0.2

            if self.keyboardState[pg.K_UP]: # set simulation speed to max
                self.simulationSleep = MIN_SIMULATION_SLEEP
                self.waitSimulationSpeedChange = 0.2

            if self.keyboardState[pg.K_DOWN]: # set simulation speed to min
                self.simulationSleep = MAX_SIMULATION_SLEEP
                self.waitSimulationSpeedChange = 0.2
        else:
            self.waitSimulationSpeedChange -= delta

        # Make simulation run
        if self.runSimulation:
            if self.simulationSleepRemain <= 0:
                self.grid.simulateStep()
                self.simulationSleepRemain = self.simulationSleep
            else:
                self.simulationSleepRemain -= delta

        # Make simulation step
        elif pg.K_RCTRL in self.keyDown:
            self.grid.simulateStep()

        # Fps cap
        if pg.K_f in self.keyDown:
            if self.fps == FPS_CAP:
                self.fps = MAX_FPS_CAP
            else:
                self.fps = FPS_CAP

        # pg.display.set_caption(f"fps : {self.clock.get_fps():.2f}")
        if self.waitFpsPrint <= 0:
            print(f"fps : {self.clock.get_fps():.2f}")
            self.waitFpsPrint = 1
        else:
            self.waitFpsPrint -= delta


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


print()
print("COMMANDS :")
print(" - mouse wheel UP -> zoom in grid")
print(" - mouse wheel DOWN -> zoom out grid")
print(" - key B -> enable / disable drawing of tiles' border")
print(" - key W/Z -> move grid down")
print(" - key S -> move grid up")
print(" - key A/Q -> move grid right")
print(" - key D -> move grid left")
print(" - key C -> clear grid")
print(" - key R -> add tile at random position")
print(" - key SPACE -> start/stop simulation")
print(" - key LEFT -> increase simulation speed")
print(" - key RIGHT -> decrease simulation speed")
print(" - key UP -> set simulation speed to max")
print(" - key DOWN -> set simulation speed to min")
print(" - key R_CTRL -> simulation step")
print(" - key F -> enable / disable fps cap")
print()

Game().run() # Start game
