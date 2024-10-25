import pygame as pg

from pygame.math import Vector2 as vec2
from define import  NB_W_TILE, NB_H_TILE,\
                    MIN_TILE_SIZE, START_TILE_SIZE, MAX_TILE_SIZE, ZOOM_SPEED,\
                    TILE_FILL_COLOR, TILE_EMPTY_COLOR, CAMERA_SPEED,\
                    WIN_W, WIN_H

class    Grid:
    def __init__(self) -> None:
        self.clear()

        self.drawTileBorder = True
        self.tileSize = START_TILE_SIZE

        self.offsetX = 0
        self.offsetY = 0


    def clear(self):
        self.tiles = []
        for _ in range(NB_H_TILE):
            self.tiles.append([0] * NB_W_TILE)


    def moveOffset(self, dir: str):
        if dir == 'u':
            self.offsetY -= CAMERA_SPEED
        elif dir == 'd':
            self.offsetY += CAMERA_SPEED
        elif dir == 'l':
            self.offsetX -= CAMERA_SPEED
        elif dir == 'r':
            self.offsetX += CAMERA_SPEED

        self.offsetX %= NB_W_TILE
        self.offsetY %= NB_H_TILE


    def zoomIn(self):
        self.tileSize = max(MIN_TILE_SIZE, self.tileSize - ZOOM_SPEED)


    def zoomOut(self):
        self.tileSize = min(MAX_TILE_SIZE, self.tileSize + ZOOM_SPEED)


    def switchDrawTileBorder(self):
        self.drawTileBorder = not self.drawTileBorder


    def handleMouseClick(self, mousePos: tuple[int], value: int):
        tileX = (mousePos[0] // self.tileSize) + self.offsetX
        tileY = (mousePos[1] // self.tileSize) + self.offsetY
        self.set(tileX, tileY, value)


    def set(self, x: int, y: int, value: int):
        x %= NB_W_TILE
        y %= NB_H_TILE

        self.tiles[y][x] = value


    def get(self, x: int, y: int) -> int:
        x %= NB_W_TILE
        y %= NB_H_TILE

        return self.tiles[y][x]


    def draw(self, win: pg.Surface):
        colors = [TILE_EMPTY_COLOR, TILE_FILL_COLOR]

        for y in range(NB_H_TILE):
            drawY = y * self.tileSize
            drawRY = (y + 1) * self.tileSize
            for x in range(NB_W_TILE):
                drawX = x * self.tileSize
                if drawX > WIN_W:
                    break

                drawRX = (x + 1) * self.tileSize
                drawRect = (drawX, drawY, self.tileSize, self.tileSize)

                tileStatus = self.get(x + self.offsetX, y + self.offsetY)

                pg.draw.rect(win, colors[tileStatus], drawRect)
                if self.drawTileBorder:
                    tileStatus = not tileStatus
                    pg.draw.line(win, colors[tileStatus], (drawX, drawY), (drawRX, drawY))
                    pg.draw.line(win, colors[tileStatus], (drawX, drawY), (drawX, drawRY))

            if drawY > WIN_H:
                break


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
