import pygame as pg
import random

from define import  NB_W_TILE, NB_H_TILE,\
                    MIN_TILE_SIZE, START_TILE_SIZE, MAX_TILE_SIZE, ZOOM_SPEED,\
                    TILE_FILL_COLOR, TILE_EMPTY_COLOR, CAMERA_SPEED,\
                    WIN_W, WIN_H

class    Grid:
    def __init__(self) -> None:

        self.drawTileBorder = True
        self.tileSize = MIN_TILE_SIZE
        # self.tileSize = START_TILE_SIZE

        self.surface = pg.Surface((NB_W_TILE * MIN_TILE_SIZE,
                                   NB_H_TILE * MIN_TILE_SIZE))

        self.cameraX = 0
        self.cameraY = 0
        self.colors = [TILE_EMPTY_COLOR, TILE_FILL_COLOR]

        self.maxCameraX = self.tileSize * NB_W_TILE
        self.maxCameraY = self.tileSize * NB_H_TILE

        self.clear()


    def clear(self):
        self.tiles = []
        for _ in range(NB_H_TILE):
            self.tiles.append([0] * NB_W_TILE)
        self.computeSurface()


    def addRandomTile(self):
        tileX = random.randint(0, NB_W_TILE - 1)
        tileY = random.randint(0, NB_H_TILE - 1)
        self.tiles[tileY][tileX] = 1
        self.computeSurface()


    def moveCamera(self, dir: str, delta: float):
        if dir == 'u':
            self.cameraY -= CAMERA_SPEED * delta
        elif dir == 'd':
            self.cameraY += CAMERA_SPEED * delta
        elif dir == 'l':
            self.cameraX -= CAMERA_SPEED * delta
        elif dir == 'r':
            self.cameraX += CAMERA_SPEED * delta

        self.cameraX %= self.maxCameraX
        self.cameraY %= self.maxCameraY


    def zoomIn(self):
        self.tileSize = max(MIN_TILE_SIZE, self.tileSize - ZOOM_SPEED)
        self.computeSurface()
        self.maxCameraX = self.tileSize * NB_W_TILE
        self.maxCameraY = self.tileSize * NB_H_TILE


    def zoomOut(self):
        self.tileSize = min(MAX_TILE_SIZE, self.tileSize + ZOOM_SPEED)
        self.computeSurface()
        self.maxCameraX = self.tileSize * NB_W_TILE
        self.maxCameraY = self.tileSize * NB_H_TILE


    def switchDrawTileBorder(self):
        self.drawTileBorder = not self.drawTileBorder
        self.computeSurface()


    def handleMouseClick(self, mousePos: tuple[int], value: int):
        tileX = (mousePos[0] - int(self.cameraX)) // self.tileSize
        tileY = (mousePos[1] - int(self.cameraY)) // self.tileSize
        self.set(tileX, tileY, value)


    def set(self, x: int, y: int, value: int):
        x %= NB_W_TILE
        y %= NB_H_TILE

        self.tiles[y][x] = value
        self.computeTileChange(x, y, value)


    def get(self, x: int, y: int) -> int:
        x %= NB_W_TILE
        y %= NB_H_TILE

        return self.tiles[y][x]


    def draw(self, win: pg.Surface):
        # Draw top left
        drawX = self.cameraX - self.maxCameraX
        drawY = self.cameraY - self.maxCameraY
        win.blit(self.surface, (drawX, drawY))

        # Draw bottom left
        drawX = self.cameraX - self.maxCameraX
        drawY = self.cameraY
        win.blit(self.surface, (drawX, drawY))

        # Draw top right
        drawX = self.cameraX
        drawY = self.cameraY - self.maxCameraY
        win.blit(self.surface, (drawX, drawY))

        # Draw bottom right
        drawX = self.cameraX
        drawY = self.cameraY
        win.blit(self.surface, (drawX, drawY))


    def computeSurface(self):
        for y in range(NB_H_TILE):
            drawY = y * self.tileSize
            drawRY = (y + 1) * self.tileSize
            for x in range(NB_W_TILE):
                drawX = x * self.tileSize

                drawRX = (x + 1) * self.tileSize
                drawRect = (drawX, drawY, self.tileSize, self.tileSize)

                tileStatus = self.get(x, y)

                pg.draw.rect(self.surface, self.colors[tileStatus], drawRect)
                if self.drawTileBorder:
                    tileStatus = not tileStatus
                    pg.draw.line(self.surface, self.colors[tileStatus], (drawX, drawY), (drawRX, drawY))
                    pg.draw.line(self.surface, self.colors[tileStatus], (drawX, drawY), (drawX, drawRY))


    def computeTileChange(self, x: int, y: int, value: int):
        drawX = x * self.tileSize
        drawRX = (x + 1) * self.tileSize
        drawY = y * self.tileSize
        drawRY = (y + 1) * self.tileSize
        drawRect = (drawX, drawY, self.tileSize, self.tileSize)

        pg.draw.rect(self.surface, self.colors[value], drawRect)
        if self.drawTileBorder:
            value = not value
            pg.draw.line(self.surface, self.colors[value], (drawX, drawY), (drawRX, drawY))
            pg.draw.line(self.surface, self.colors[value], (drawX, drawY), (drawX, drawRY))


    def simulateStep(self):
        changes = []

        # Detect changes
        for y in range(NB_H_TILE):
            pY = (y - 1) % NB_H_TILE # previous y
            nY = (y + 1) % NB_H_TILE # next y

            for x in range(NB_W_TILE):
                pX = (x - 1) % NB_W_TILE # previous x
                nX = (x + 1) % NB_W_TILE # next x

                # Get number of tile fill in neighborhood
                neighborsValue = 0
                neighborsValue += self.tiles[pY][pX]
                neighborsValue += self.tiles[pY][x]
                neighborsValue += self.tiles[pY][nX]
                neighborsValue += self.tiles[y][pX]
                neighborsValue += self.tiles[y][nX]
                neighborsValue += self.tiles[nY][pX]
                neighborsValue += self.tiles[nY][x]
                neighborsValue += self.tiles[nY][nX]

                tileStatus = self.tiles[y][x]

                # If an empty tile is have 3 fill tile around, make it fill
                if tileStatus == 0 and neighborsValue == 3:
                    changes.append((x, y, 1)) # add the change

                # If an fill tile is haven't 2 or 3 fill tile around, make it empty
                if tileStatus == 1 and neighborsValue != 2 and neighborsValue != 3:
                    changes.append((x, y, 0)) # add the change

        # Apply changes
        for x, y, value in changes:
            self.tiles[y][x] = value
            self.computeTileChange(x, y, value)
